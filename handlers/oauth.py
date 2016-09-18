# -*- coding: utf-8 -*-

"""
    alter by: youfaNi
    alter on 2016-07-13
"""
import json,pdb
import oauth2
import oauth2.tokengenerator
import oauth2.grant
import oauth2.store.redisdb
import oauth2.store.mongodb
from oauth2.web.tornado import OAuth2Handler
import json
import time
import pymongo
from dhuicredit.app import get_options
import dhuicredit.libs.utils as utils
import dhuicredit.model.oauth as oauth
import dhuicredit.libs.utils as utils
import dhuicredit.authority as Authority

auth_provider = None
def init_oauth(*args,**options):
    # Init auth_provider only once
    global auth_provider
    if auth_provider :
        return auth_provider
    # Populate mock
    oauth_model = oauth.OauthModel()
    coll = oauth_model.get_coll()
    client_store = oauth2.store.mongodb.ClientStore(coll)

    # Redis for tokens storage
    token_store = oauth2.store.redisdb.TokenStore(rs=utils.Redis())

    # Generator of tokens
    token_generator = oauth2.tokengenerator.Uuid4()
    token_generator.expires_in[oauth2.grant.ClientCredentialsGrant.grant_type] = 3600

    # OAuth2 controller
    auth_provider = oauth2.Provider(
        access_token_store=token_store,
        auth_code_store=token_store,
        client_store=client_store,
        token_generator=token_generator
    )
    # auth_controller.token_path = '/oauth/token'

    # Add Client Credentials to OAuth2 controller
    scopes_config = options.get("scopes_config")
    default_scope = scopes_config[0] # token默认具有的权限
    scopes = scopes_config[1] # token 可获得的权限
    auth_provider.add_grant(oauth2.grant.ClientCredentialsGrant(default_scope=default_scope,scopes=scopes))

    return auth_provider

scopes_config = Authority.authority.get_scopes()
handlers = [
                (r'/token', OAuth2Handler,init_oauth(scopes_config=scopes_config["all"])),
            ]
