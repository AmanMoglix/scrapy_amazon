#-*- coding: utf-8 -*-
# any thing you want
from operator import le
import re
import scrapy
import sys
import random


 


class AmazonSpider(scrapy.Spider):
    name = 'amazon1000'
 
    abc=open('/home/moglix/Desktop/amazon1000.txt').read().splitlines()

    start_urls=abc
    
    def parse(self, response):
        data={}
        
        r1=(response.xpath("//div[contains(@class,'a-section')]/div[contains(@class,'sg-row')]")).getall()
        #r1=(response.xpath("//a[contains(@class,'a-link-normal s-no-outline')]/@href")).getall()
        print(len(r1))
        if(len(r1)==1):
            r1=(response.xpath("//div[contains(@class,'a-section a-spacing-base')]")).getall()

        p_id=''
        substring="/dp"
        sub_sponsered="Sponsored"
        amzaon_url="https://www.amazon.in/dp/"
        intem_start=0
        for ret in r1:
              if substring in ret:
               #print(intem_start)
               if intem_start <5: 
                 pid_str=re.split('dp/',ret)[1]
                 product_id=re.split('/ref',pid_str)[0]
                 if product_id in p_id:
                   #print("exist "+product_id)
                   continue
                 else:
                     #print("hellao "+ret)
                     #check the prdouctID is sponsered or not
                     if sub_sponsered in ret:
                         print( " id sponsered sponserd ")
                         continue
                     else:
                         intem_start=intem_start+1
                         print("intem_start",intem_start)
                         if(len(p_id)==0):
                           p_id=amzaon_url+product_id.strip()
                           print("Non Sponsered productId"+p_id)
                         
               else:
                   #print("break")
                   break
        #add to failed url
        #print(len(p_id))
        if len(p_id)==0 :
             filet=open('failed_netmart.txt','a')
             filet.write(str(response.url)+"\n")
        
        data={
            'Product_Id':p_id,
            'url':response.url
        }
        
        yield data

