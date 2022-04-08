#-*- coding: utf-8 -*-
# any thing you want
from operator import le
from urllib import response
import scrapy
import sys
import random
import re


 


class AmazonSpider(scrapy.Spider):
    name = 'amazonp2000'
 
    abc=open('/home/moglix/Desktop/amazonp2000.txt').read().splitlines()

    start_urls=abc
    
    def parse(self, response):
        data={}
        title=response.xpath('//h1[@id="title"]/span/text()').get()
        l1=response.xpath('//*[@class="a-unordered-list a-nostyle a-horizontal a-size-base"]/li[1]/span/a/text()').get()
        print(l1)
        if title == None:
           product_name=l1
        

        review_content=(response.xpath("//*[contains(@class,'a-section review aok-relative')]//*[contains(@class,'a-section celwidget')]//*[contains(@class,'a-row')]//*[contains(@class,'a-icon a-icon-star')]/span/text()")).extract()
        #review_comment=(response.xpath("//*[contains(@class,'a-row a-spacing-small review-data')]//*[contains(@class,'a-size-base review-text')]/span/text()")).getall()
        #pdp page
        #review_comment=(response.xpath("//*[contains(@class,'a-expander-content reviewText review-text-content a-expander-partial-collapse-content')]")).extract()
        #review page
        review_comment=(response.xpath("//*[contains(@class,'a-size-base review-text review-text-content')]")).extract()

        print("review lenght")
        print(len(review_content))

        print("review comment")
        print(len(review_comment))
        review_tuple={}
        if(len(review_comment)== len(review_content)):
         index=0
         for review_data in review_content:
                review_key=re.split('out',review_data)[0]
                #print(review_key)
                review_tuple[review_comment[index]]=review_key
                index=index+1
        #  for review_c in review_comment:
        #             review_comment_data=review_c.split('<span>')[1].split('</span>')[0]
        #             print(review_comment_data)

        r_1=''
        r_2=''
        r_3=''
        r_4=''
        r_5=''
        r_6=''
        r_7=''
        r_8=''
        r_9=''
        r_10=''
        for i in review_tuple.keys():
            #to check rating 
            if(float(review_tuple.get(i))>=4):
                r_data=i.split('<span>')[1].split('</span>')[0].replace("<br>","").encode('ascii', 'ignore').decode('ascii')
                #capture the word count
                word_count=len(r_data.split())
                print("word count ",word_count)
                print(r_data,review_tuple.get(i))
                #add flag for the word count
                if(float(word_count)<135):
                 if(len(r_1)==0):
                     r_1=r_data
                     continue
                 if(len(r_2)==0):
                     r_2=r_data
                     continue
                 if(len(r_3)==0):
                     r_3=r_data
                     continue
                 if(len(r_4)==0):
                     r_4=r_data
                     continue
                 if(len(r_5)==0):
                     r_5=r_data
                     continue
                 if(len(r_6)==0):
                     r_6=r_data
                     continue
                 if(len(r_7)==0):
                     r_7=r_data
                     continue
                 if(len(r_8)==0):
                     r_8=r_data
                     continue
                 if(len(r_9)==0):
                     r_9=r_data
                     continue
                 if(len(r_10)==0):
                     r_10=r_data


        #if review is not found
        if(len(r_1)==0 and len(product_name)==0):
            filet=open('failed_netmart.txt','a')
            filet.write(str(response.url)+"\n")         
                
       
        
        data={
            'Product_Name':product_name,
            'Url':response.url,
            'r_1':r_1,
            'r_2':r_2,
            'r_3':r_3,
            'r_4':r_4,
            'r_5':r_5,
            'r_6':r_6,
            'r_7':r_7,
            'r_8':r_8,
            'r_9':r_9,
            'r_10':r_10

        }
        
        yield data
