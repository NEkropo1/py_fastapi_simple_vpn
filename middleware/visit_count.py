from collections import defaultdict


class VisitCountMiddleware:
    def __init__(self, app):
        self.app = app
        self.visit_counts = defaultdict(int)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            self.visit_counts[scope["path"]] += 1
        await self.app(scope, receive, send)
