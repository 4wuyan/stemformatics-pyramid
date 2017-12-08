class Helper:
    #h.url is not in use right now
    def url(self,url_string):
        return None
    def external_dependency_url(self,url_string,url_string2):
        return "https://"+url_string
    def web_asset_url(self,url_string):
        return "file:///public"+url_string