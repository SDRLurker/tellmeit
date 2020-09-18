#!/usr/bin/python3
#-*- coding: utf-8 -*-
import logging
import logging.handlers
import os

def get_logger(name):
    pwd = os.getcwd()
    if not os.path.exists('%s/log' % pwd):
        os.makedirs('%s/log' % pwd)
    # logger 인스턴스를 생성 및 로그 레벨 설정
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    # fileHandler와 StreamHandler를 생성
    fileHandler = logging.FileHandler('./log/my.log')
    # handler에 fommater 세팅
    fileHandler.setFormatter(formatter)
    # Handler를 logging에 추가
    logger.addHandler(fileHandler)
    # 콘솔 출력 핸들러(https://hamait.tistory.com/880)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
