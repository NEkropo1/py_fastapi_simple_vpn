from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, get_session=None, site=None):
        super().__init__(app=app)
        self.get_session = get_session
        self.Site = site

    async def dispatch(self, request: Request, call_next):
        request_body = await request.body()
        response = await call_next(request)
        if response.status_code == 200 and self.get_session and self.Site:
            try:
                site_url = request.url.path
                content_length = int(response.headers.get("content-length", 0))
                if content_length > 0:
                    with self.get_session() as session:
                        site = session.query(self.Site).filter(self.Site.url == site_url).first()
                        if site:
                            site.data_uploaded += len(request_body)
                            site.data_downloaded += content_length
            except Exception as e:
                print(f"Error: {e}")
        return response
