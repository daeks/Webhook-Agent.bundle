import hashlib, os, time

def Start():
  pass
  
def ValidatePrefs():
  pass

class WebhookAgent(Agent.Movies):

  name = 'Webhook Metadata Agent'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.development','com.plexapp.agents.none']

  def search(self, results, media, lang):

    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):
  
    if Prefs['webhook']:
      if Prefs['combined']:
        Log('Loading data of contributer combined')
        self.hook(media, metadata.contribution('_combined'))

      if Prefs['contributors']:
        for contributor in metadata.contributors:
          if contributor.startswith('com.'):
            Log('Loading data of contributer %s' % contributor)
            self.hook(media, metadata.contribution(contributor))
            
  def hook(self, media, data):
    part = media.items[0].parts[0]
    path = os.path.dirname(part.file)
    (root_file, ext) = os.path.splitext(os.path.basename(part.file))
  
    output = {}
    output['event'] = 'metadata.update'
    output['root_file'] = root_file
    output['ext'] = ext

    for key, obj in data.attrs.items():
      if isinstance(obj, Framework.modelling.attributes.StringObject):
        output[key] = getattr(data, key)
      elif isinstance(obj, Framework.modelling.attributes.IntegerObject):
        output[key] = getattr(data, key)
      elif isinstance(obj, Framework.modelling.attributes.FloatObject):
          output[key] = getattr(data, key)
      else:
        pass
   
    jdata = JSON.StringFromObject(output)
    
    Log('Parsed metadata to JSON String %s' % jdata)
    Log('Sending payload to %s' % Prefs['webhook'])
    post_values = {'payload': jdata}
    result = HTTP.Request(Prefs['webhook'], values=post_values)

  def dump(self, obj):
    for attr in dir(obj):
      Log('obj.%s = %s' % (attr, getattr(obj, attr)))
