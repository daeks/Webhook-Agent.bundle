import os 

def Start():
  pass
  
def ValidatePrefs():
  pass

def dump(self, obj):
  for attr in dir(obj):
    Log('[HOOK] obj.%s = %s' % (attr, getattr(obj, attr)))
  Log('[HOOK] obj has been dumped')

class WebhookAgent(Agent.Movies):

  name = 'Webhook Metadata Agent (Movies)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.none', 'com.plexapp.agents.imdb', 'com.plexapp.agents.themoviedb']

  def search(self, results, media, lang):
    if media.primary_agent == 'com.plexapp.agents.none':
      results.Append(MetadataSearchResult(id = media.id, name = media.name, score = 100))
    else:
      results.Append(MetadataSearchResult(id = media.primary_metadata.id, score = 100))

  def update(self, metadata, media, lang):
    if Prefs['webhook']:
      if Prefs['combined']:
        Log('[HOOK] Loading data of contributer combined')
        self.hook(media, metadata, '_combined')

      if Prefs['contributors']:
        for contributor in metadata.contributors:
          if contributor.startswith('com.'):
            Log('[HOOK] Loading data of contributer %s' % contributor)
            self.hook(media, metadata, contributor)
            
  def hook(self, media, metadata, contributor):
    part = media.items[0].parts[0]
    path = os.path.dirname(part.file)
    (root_file, ext) = os.path.splitext(os.path.basename(part.file))
  
    data = metadata.contribution(contributor)
  
    output = {}
    output['event'] = 'metadata.update'
    output['type'] = 'agent.movies'
    output['provider'] = str(data.provider)
    output['id'] = data.id
    output['guid'] = data.guid
    output['root_file'] = root_file
    output['ext'] = ext
    
    if contributor is '_combined':
      primary_contributor = data.guid.split(':')[0]
      Log('[HOOK] Loading data of primary contributer %s' % primary_contributor)
      primary_data = metadata.contribution(primary_contributor)
      
      output['posters'] = {}
      i = 0
      for obj in data.posters:
        output['posters'][i] = obj
        i += 1
        
      output['art'] = {}
      i = 0
      for obj in data.art:
        output['art'][i] = obj
        i += 1
      
      for key, obj in primary_data.attrs.items():
        if isinstance(obj, Framework.modelling.attributes.StringObject):
          output[key] = str(getattr(primary_data, key)).replace('"', '')
        elif isinstance(obj, Framework.modelling.attributes.IntegerObject):
          output[key] = getattr(primary_data, key)
        elif isinstance(obj, Framework.modelling.attributes.FloatObject):
            output[key] = getattr(primary_data, key)
        else:
          pass

    for key, obj in data.attrs.items():
      if isinstance(obj, Framework.modelling.attributes.StringObject):
        if not getattr(data, key) is None:
          output[key] = str(getattr(data, key)).replace('"', '')
      elif isinstance(obj, Framework.modelling.attributes.IntegerObject):
        if not getattr(data, key) is None:
          output[key] = getattr(data, key)
      elif isinstance(obj, Framework.modelling.attributes.FloatObject):
        if not getattr(data, key) is None:
          output[key] = getattr(data, key)
      else:
        pass
   
    jdata = JSON.StringFromObject(output)
    
    Log('[HOOK] Parsed metadata to JSON String %s' % jdata)
    Log('[HOOK] Sending payload to %s' % Prefs['webhook'])
    post_values = {'payload': jdata}
    result = HTTP.Request(Prefs['webhook'], values=post_values)
      
class WebhookAgent(Agent.TV_Shows):

  name = 'Webhook Metadata Agent (TV)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.none', 'com.plexapp.agents.thetvdb', 'com.plexapp.agents.themoviedb']

  def search(self, results, media, lang):
    if media.primary_agent == 'com.plexapp.agents.none':
      results.Append(MetadataSearchResult(id = media.id, name = media.show, score = 100))
    else:
      results.Append(MetadataSearchResult(id = media.primary_metadata.id, score = 100))

  def update(self, metadata, media, lang):
    if Prefs['webhook']:
      if Prefs['combined']:
        Log('[HOOK] Loading data of contributer combined')
        self.hook(media, metadata, '_combined')

      if Prefs['contributors']:
        for contributor in metadata.contributors:
          if contributor.startswith('com.'):
            Log('[HOOK] Loading data of contributer %s' % contributor)
            self.hook(media, metadata, contributor)
            
  def hook(self, media, metadata, contributor):
    part = media.children[0].children[0].items[0].parts[0]
    path = os.path.dirname(part.file)
    (root_file, ext) = os.path.splitext(os.path.basename(part.file))
  
    data = metadata.contribution(contributor)
  
    output = {}
    output['event'] = 'metadata.update'
    output['type'] = 'agent.tv_shows'
    output['provider'] = str(data.provider)
    output['id'] = media.id
    output['guid'] = data.guid
    output['root_file'] = root_file
    output['ext'] = ext
    
    output['season_count'] = len(media.seasons)
    i = 0
    for snum, season in media.seasons.iteritems():
      for enum, episode in season.episodes.iteritems():
        i += 1
    output['episode_count'] = i
      
    if contributor is '_combined':
      primary_contributor = data.guid.split(':')[0]
      Log('[HOOK] Loading data of primary contributer %s' % primary_contributor)
      primary_data = metadata.contribution(primary_contributor)
      
      output['posters'] = {}
      i = 0
      for obj in primary_data.posters:
        output['posters'][i] = obj
        i += 1
        
      output['art'] = {}
      i = 0
      for obj in primary_data.art:
        output['art'][i] = obj
        i += 1
           
      for key, obj in primary_data.attrs.items():
        if isinstance(obj, Framework.modelling.attributes.StringObject):
          output[key] = str(getattr(primary_data, key)).replace('"', '')
        elif isinstance(obj, Framework.modelling.attributes.IntegerObject):
          output[key] = getattr(primary_data, key)
        elif isinstance(obj, Framework.modelling.attributes.FloatObject):
          output[key] = getattr(primary_data, key)
        else:
          pass

    for key, obj in data.attrs.items():
      if isinstance(obj, Framework.modelling.attributes.StringObject):
        if not getattr(data, key) is None:
          output[key] = str(getattr(data, key)).replace('"', '')
      elif isinstance(obj, Framework.modelling.attributes.IntegerObject):
        if not getattr(data, key) is None:
          output[key] = getattr(data, key)
      elif isinstance(obj, Framework.modelling.attributes.FloatObject):
        if not getattr(data, key) is None:
          output[key] = getattr(data, key)
      else:
        pass
        
      output['seasons'] = {}
      output['episodes'] = {}
      for snum, season in media.seasons.iteritems():
        tmp = {}
        tmp['index'] = snum
        tmp['id'] = season.id
        tmp['index'] = season.index
        tmp['originallyAvailableAt'] = season.originallyAvailableAt
        tmp['originally_available_at'] = season.originally_available_at
        tmp['parentTitle'] = season.parentTitle
        tmp['title'] = season.title
        tmp['posters'] = {}
        i = 0
        for obj in primary_data.seasons[season.index].posters:
          tmp['posters'] = obj
          i += 1
        i = 0
        for enum, episode in season.episodes.iteritems():
          i += 1
        tmp['episodes'] = i
        output['seasons'][snum] = tmp
        
        output['episodes'][snum] = {}
        for enum, episode in season.episodes.iteritems():
          tmp = {}
          tmp['guid'] = episode.guid
          tmp['id'] = episode.id
          tmp['index'] = episode.index
          tmp['originallyAvailableAt'] = episode.originallyAvailableAt
          tmp['originally_available_at'] = episode.originally_available_at
          tmp['parentTitle'] = episode.parentTitle
          tmp['title'] = episode.title
          output['episodes'][snum][enum] = tmp
    
    jdata = JSON.StringFromObject(output)
    
    Log('[HOOK] Parsed metadata to JSON String %s' % jdata)
    Log('[HOOK] Sending payload to %s' % Prefs['webhook'])
    post_values = {'payload': jdata}
    result = HTTP.Request(Prefs['webhook'], values=post_values)
