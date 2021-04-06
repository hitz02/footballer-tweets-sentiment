from django.shortcuts import render
from django.http import HttpResponse
from .models import Twitter_Handles, Tweets, Sentiment
from django.db.models import Count
import json


def index(request):
    return render(request,'index.html')

def help(request):
    return render(request,'help.html')
    

def show_team(request):
    team_name = request.GET.get('team_name')
    team_data = Twitter_Handles.objects.filter(team_name=team_name)
    team_tweets = list(Tweets.objects.filter(player_name=team_name).order_by('-created_at').values_list('tweet',flat=True))[:5]
    return render(request,'teams.html',{'team':team_data,'team_tweets':team_tweets,'team_name':team_name})

def show_player(request):
    player_name = request.GET.get('player_name')
    player_data_no_covid = Sentiment.objects.filter(player_name=player_name,covid_time=0).values('sentiment').order_by('sentiment').annotate(count=Count('sentiment'))
    player_data_covid = Sentiment.objects.filter(player_name=player_name,covid_time=1).values('sentiment').order_by('sentiment').annotate(count=Count('sentiment'))

    no_covid_dict = dict([list(k.values()) for k in player_data_no_covid])
    covid_dict = dict([list(k.values()) for k in player_data_covid])

    categories = ['positive','neutral','negative']
    no_covid_counts = [no_covid_dict.get('positive',0),no_covid_dict.get('neutral',0),no_covid_dict.get('negative',0)]
    covid_counts = [covid_dict.get('positive',0),covid_dict.get('neutral',0),covid_dict.get('negative',0)]

    insight = ''

    if all(v == 0 for v in no_covid_counts) and all(v == 0 for v in covid_counts):
        insight = 'No Tweets to compare for {}'.format(player_name)
    elif ~all(v == 0 for v in no_covid_counts) and all(v == 0 for v in covid_counts):
        MaxKey = max(no_covid_dict, key=no_covid_dict.get)
        insight = '{} had more {} tweets before pandemic'.format(player_name,MaxKey)
    elif all(v == 0 for v in no_covid_counts) and ~all(v == 0 for v in covid_counts):
        MaxKey = max(covid_dict, key=covid_dict.get)
        insight = '{} had more {} tweets after pandemic'.format(player_name,MaxKey)
    else:
        MaxKey1 = max(no_covid_dict, key=no_covid_dict.get)
        MaxKey2 = max(covid_dict, key=covid_dict.get)
        if MaxKey1==MaxKey2:
            if no_covid_dict.get(MaxKey1,0)>=covid_dict.get(MaxKey2,0):
                insight = '{} was more {} when using twitter before pandemic'.format(player_name,MaxKey1)
            else:
                insight = '{} was more {} when using twitter after pandemic'.format(player_name,MaxKey1)
        else:
            insight = '{} was more {} when using twitter before pandemic and more {} after pandemic'.format(player_name,MaxKey1,MaxKey2)

    before_covid_series = {
        'name': 'Before COVID',
        'data': no_covid_counts,
        'color': 'blue'
    }

    after_covid_series = {
        'name': 'After COVID',
        'data': covid_counts,
        'color': 'orange'
    }

    title = 'Sentiment Distribution of Tweets for {}'.format(player_name)

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': title},
        'xAxis': {'categories': categories},
        'series': [before_covid_series, after_covid_series]
        }

    dump = json.dumps(chart)

    return render(request, 'player.html', {'chart': dump,'player_name':player_name,'insight':insight})