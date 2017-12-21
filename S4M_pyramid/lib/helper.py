class Helper:
    def __init__(self,request,site_url):
        self.request=request
        self.site_url=site_url

    def url(self,url_string):
        return self.site_url+url_string

    def external_dependency_url(self,url_string,url_string2):
        return "https://"+url_string

    def web_asset_url(self,url_string):
        return self.request.static_url("S4M_pyramid:public"+url_string)