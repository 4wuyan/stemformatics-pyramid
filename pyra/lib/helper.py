class Helper:
    def __init__(self,request):
        self.request=request
    #h.url is not in use right now
    def url(self,url_string):
        return None
    def external_dependency_url(self,url_string,url_string2):
        return "https://"+url_string
    def web_asset_url(self,url_string):
        site_name="www-pyramid1.stemformatics.org"
        return site_name+"/screen/"+url_string