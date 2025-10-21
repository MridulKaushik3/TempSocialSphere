from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse
from .models import Tweet, Comment, Like
from .forms import TweetForm, UserRegistrationForm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Simple home view
def home(request):
    return HttpResponse("Welcome to SocialSphere!")

# Optional index view if used
def index(request):
    return render(request, 'index.html')

# List all tweets (search enabled)
def tweet_list(request):
    
    query = request.GET.get('q', '')
    tweets = Tweet.objects.filter(text__icontains=query) if query else Tweet.objects.all()
    tweets = tweets.order_by('-created_at')

    # Handle comment POST
    if request.method == 'POST' and request.user.is_authenticated:
        tweet_id = request.POST.get('tweet_id')
        comment_text = request.POST.get('comment')
        if tweet_id and comment_text:
            tweet = get_object_or_404(Tweet, id=tweet_id)
            Comment.objects.create(tweet=tweet, user=request.user, text=comment_text)
            return redirect('tweet_list')

    return render(request, 'tweet_list.html', {'tweets': tweets})


def analyze_tone(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    if score['compound'] >= 0.05:
        return 'non-toxic'
    elif score['compound'] <= -0.05:
        return 'toxic'
    else:
        return 'neutral'

# Create a new tweet
@login_required(login_url='/accounts/login/')
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.tone = analyze_tone(tweet.text)
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

# Edit an existing tweet
@login_required(login_url='/accounts/login/')
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

# Delete a tweet
@login_required(login_url='/accounts/login/')
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

# User registration
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    # Check if the user already liked the tweet
    already_liked = Like.objects.filter(user=request.user, tweet=tweet).exists()

    if not already_liked:
        Like.objects.create(user=request.user, tweet=tweet)
    
    return redirect('tweet_list')