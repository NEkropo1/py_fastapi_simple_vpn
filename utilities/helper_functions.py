from typing import Optional

import fastapi

import models


def get_user_by_username(session, username) -> Optional[models.User]:
    return session.query(models.User).filter(models.User.username == username).first()


def get_site_data(user):
    if user:
        sites_data = {
            site.url: {
                "follow_counter": site.follow_counter,
                "data_uploaded": site.data_uploaded,
                "data_downloaded": site.data_downloaded
            } for site in user.sites
        }
        return sites_data if sites_data else {"message": "No sites created yet."}
    else:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
