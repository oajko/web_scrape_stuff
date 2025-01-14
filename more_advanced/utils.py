from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random

class RotateProxy(HttpProxyMiddleware):
    def __init__(self,settings,*args,**kwargs):
        super(RotateProxy,self).__init__(*args,**kwargs)
        self.proxies=settings.get('ROTATING_PROXY_LIST',[])

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def process_request(self,request,spider):
        if self.proxies:
            proxy=random.choice(self.proxies)
            request.meta['proxy']=proxy
    
    def process_exception(self,request,exception,spider):
        if self.proxies:
            proxy=random.choice(self.proxies)
            request.meta['proxy']=proxy
            return request
    
    def process_response(self,request,response,spider):
        if response.status in [403,429]:
            proxy=random.choice(self.proxies)
            request.meta['proxy']=proxy
            return request
        return response

class RotateAgent(UserAgentMiddleware):
    def __init__(self,settings,*args,**kwargs):
        super(RotateAgent,self).__init__(*args,**kwargs)
        self.user_agent=settings.get('USER_AGENT_LIST',[])
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if self.user_agent:
            agent=random.choice(self.user_agent)
            request.headers['User-Agent']=agent
