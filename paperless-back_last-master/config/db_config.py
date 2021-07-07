#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from config.lib import *
from config.value import *



if type_product == 'uat':
    # paper_less_uat.config["SQLALCHEMY_BINDS"] = {
    #     "paper_less_master":"postgresql://jirayu:paperless@n12345678@10.0.1.11:5432/paper_less_uat",
    #     "paper_less_slave":"postgresql://jirayu:paperless@n12345678@10.0.1.12:5432/paper_less_uat"
    # }
    # db_init = SQLAlchemy(paper_less_uat)
    # db_init.Model_RW = db_init.make_declarative_base()
    engine = create_engine('postgresql://jirayu:paperless@n12345678@10.0.0.50:5432/paper_less_uat',pool_pre_ping=True,pool_recycle=60)
    slave = create_engine('postgresql://jirayu:paperless@n12345678@10.0.0.50:5432/paper_less_uat',pool_pre_ping=True,pool_recycle=60)
    # Session = scoped_session(sessionmaker(bind=slave))
    paper_less_uat.config["SQLALCHEMY_BINDS"] = {
         "paper_less_uat":"postgresql://jirayu:paperless@n12345678@10.0.0.50:5432/paper_less_uat"
    }    
    paper_less_uat.config['SQLALCHEMY_ENABLE_POOL_PRE_PING'] = True
    paper_less_uat.config['SQLALCHEMY_POOLCLASS'] = 'QueuePool'
    paper_less_uat.config['SQLALCHEMY_POOL_RECYCLE'] = 60
    # paper_less_uat.config['SQLALCHEMY_POOL_SIZE'] = 200
    # paper_less_uat.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    # paper_less_uat.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    #     'SQLALCHEMY_MAX_OVERFLOW':-1,
    #     'SQLALCHEMY_POOL_SIZE':200,
    #     # 'SQLALCHEMY_POOL_RECYCLE':60,
    #     'SQLALCHEMY_POOL_RECYCLE':10
    #     # 'pool_size': 200,
    #     # 'pool_recycle': 10,
    #     # 'pool_pre_ping': True,
    #     # 'max_overflow':-1
    # }
    paper_less_uat.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_init = SQLAlchemy(paper_less_uat)
    # db_init = SQLAlchemy(
    #     engine_options={ 'connect_args': { 'connect_timeout': 1000 }}
    # )
    # db_init.init_app(paper_less_uat)
    # db_init.Model_RW = db_init.make_declarative_base()
elif type_product == 'prod':
    engine = create_engine('postgresql://jirayu:paperless@n12345678@10.0.1.10:80/paper_less_prod',pool_pre_ping=True,pool_recycle=60)
    slave = create_engine('postgresql://jirayu:paperless@n12345678@10.0.1.10:443/paper_less_prod',pool_pre_ping=True,pool_recycle=60)
    paper_less.config["SQLALCHEMY_BINDS"] = {
        "paper_less_master":"postgresql://jirayu:paperless@n12345678@10.0.1.10:80/paper_less_prod",
        "paper_less_slave":"postgresql://jirayu:paperless@n12345678@10.0.1.10:80/paper_less_prod"
    }
    # engine = create_engine('postgresql://jirayu:paperless@n12345678@10.0.1.11:5432/paper_less_prod',pool_pre_ping=True,pool_recycle=10,pool_size=200, max_overflow=-1)
    # slave = create_engine('postgresql://jirayu:paperless@n12345678@10.0.1.11:5432/paper_less_prod',pool_pre_ping=True,pool_recycle=10,pool_size=200, max_overflow=-1)
    # paper_less.config["SQLALCHEMY_BINDS"] = {
    #     "paper_less_master":"postgresql://jirayu:paperless@n12345678@10.0.1.11:5432/paper_less_prod",
    #     "paper_less_slave":"postgresql://jirayu:paperless@n12345678@10.0.1.11:5432/paper_less_prod"
    # }
    paper_less.config['SQLALCHEMY_ENABLE_POOL_PRE_PING'] = True
    paper_less.config['SQLALCHEMY_POOLCLASS'] = 'QueuePool'
    paper_less.config['SQLALCHEMY_POOL_RECYCLE'] = 60
    # paper_less.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    #     'SQLALCHEMY_MAX_OVERFLOW':-1,
    #     'SQLALCHEMY_POOL_SIZE':200,
    #     # 'SQLALCHEMY_POOL_RECYCLE':60,
    #     'SQLALCHEMY_POOL_RECYCLE':10,
    #     'SQLALCHEMY_ENABLE_POOL_PRE_PING':True
    #     # 'pool_size': 200,
    #     # 'pool_recycle': 10,
    #     # 'pool_pre_ping': True,
    #     # 'max_overflow':-1
    # }
    # paper_less.config['SQLALCHEMY_POOL_SIZE'] = 200
    # paper_less.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    # paper_less.config.update({
    #     'SQLALCHEMY_POOL_SIZE': 50,
    #     'SQLALCHEMY_MAX_OVERFLOW': 100
    # })
    paper_less.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db_init = SQLAlchemy(
    #     engine_options={ 'connect_args': { 'connect_timeout': 1000 }}
    # )
    # db_init.init_app(paper_less)
    db_init = SQLAlchemy(paper_less)
    # db_init = SQLAlchemy(paper_less , engine_options = {
    #     'connect_args' : {'connect_timeout':5}
    # }
    # )
    # db_init = SQLAlchemy(
    #     engine_options={ 'connect_args': { 'connect_timeout': 5 }}
    # )
    # db_init.Model_RW = db_init.make_declarative_base()
elif type_product == 'dev':
    engine = create_engine('postgresql://jirayu:paperless@n12345678@10.0.1.11:5432/ppl_dev')
    paper_lessdev.config["SQLALCHEMY_BINDS"] = {
         "paper_lessdev":"postgresql://paperlessdev:dev_n12345678@10.0.1.11:5432/ppl_dev"
    }
    paper_lessdev.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_init = SQLAlchemy(paper_lessdev)
    db_init.Model_RW = db_init.make_declarative_base()
elif type_product == 'poc':
    engine = create_engine('postgresql://pocppl:pbofumujwfhi^h0yd@10.0.0.41:5432/ppl_poc',pool_pre_ping=True,pool_recycle=60)
    slave = create_engine('postgresql://pocppl:pbofumujwfhi^h0yd@10.0.0.41:5432/ppl_poc',pool_pre_ping=True,pool_recycle=60)
    paper_less.config["SQLALCHEMY_BINDS"] = {
        "paper_less_master":"postgresql://pocppl:pbofumujwfhi^h0yd@10.0.0.41:5432/ppl_poc",
        "paper_less_slave":"postgresql://pocppl:pbofumujwfhi^h0yd@10.0.0.41:5432/ppl_poc"
    }
    paper_less.config['SQLALCHEMY_ENABLE_POOL_PRE_PING'] = True
    paper_less.config['SQLALCHEMY_POOLCLASS'] = 'QueuePool'
    paper_less.config['SQLALCHEMY_POOL_RECYCLE'] = 60
    paper_less.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_init = SQLAlchemy(paper_less)

