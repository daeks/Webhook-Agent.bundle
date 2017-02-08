import hashlib, os, time

def Start():
  pass
  
def ValidatePrefs():
  pass

class ExportAgent(Agent.Movies):

  name = 'Export Agent'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.none']

  def search(self, results, media, lang):

    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):
  
    if Prefs['webhook']:
      part = media.items[0].parts[0]
      path = os.path.dirname(part.file)
      (root_file, ext) = os.path.splitext(os.path.basename(part.file))

      for contributor in metadata.contributors:
        if contributor.startswith('com.'):
          Log('Loading data of contributer %s' % contributor)
          data = metadata.contribution(contributor)
          
          output = {}
          output['event'] = 'metadata'
          output['provider'] = str(data.provider)
          output['id'] = data.id
          output['guid'] = data.guid
          output['root_file'] = root_file
          output['ext'] = ext
          
          if data.title:
            output['title'] = str(data.title.encode('utf-8'))
          
          if data.summary:
            output['summary'] = str(data.summary.encode('utf-8'))
            
          if data.rating:
            output['rating'] = data.rating
            
          if data.title_sort:
            output['title_sort'] = str(data.title_sort.encode('utf-8'))
         
          jdata = JSON.StringFromObject(output)
          
          Log('Parsed metadata to JSON String %s' % jdata)
          Log('Sending payload to %s' % Prefs['webhook'])
          post_values = {'payload': jdata}
          result = HTTP.Request(Prefs['webhook'], values=post_values)

  def dump(self, obj):
    for attr in dir(obj):
      Log('obj.%s = %s' % (attr, getattr(obj, attr)))