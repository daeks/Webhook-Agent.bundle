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
    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

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
    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

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
    
    for snum, season in media.seasons.iteritems():
      output['season'] = season.index
      for enum, episode in season.episodes.iteritems():
        output['episode'] = episode.index
      
    if contributor is '_combined':
      primary_contributor = data.guid.split(':')[0]
      Log('[HOOK] Loading data of primary contributer %s' % primary_contributor)
      primary_data = metadata.contribution(primary_contributor)
      
      for snum, season in media.seasons.iteritems():
        output['posters'] = {}
        i = 0
        for obj in primary_data.seasons[season.index].posters:
          output['posters'][i] = obj
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