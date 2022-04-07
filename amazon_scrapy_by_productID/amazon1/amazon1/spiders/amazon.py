#-*- coding: utf-8 -*-
# any thing you want
from ast import Not
from operator import le
import re
from struct import pack
import scrapy
import sys
import random


 


class AmazonSpider(scrapy.Spider):
    name = 'amazonupdationerror'
 
    abc=open('/home/moglix/Desktop/amazonupdationerror.txt').read().splitlines()

    start_urls=abc
    
    def parse(self, response):
        data={}
        title=response.xpath('//h1[@id="title"]/span/text()').get()
        product_name=title
        l1=response.xpath('//*[@class="a-unordered-list a-horizontal a-size-small"]/li[1]/span/a/text()').get()
        l2=response.xpath('//*[@class="a-unordered-list a-horizontal a-size-small"]/li[3]/span/a/text()').get()
        l3=response.xpath('//*[@class="a-unordered-list a-horizontal a-size-small"]/li[5]/span/a/text()').get()
        l4=response.xpath('//*[@class="a-unordered-list a-horizontal a-size-small"]/li[7]/span/a/text()').get()
        l5=response.xpath('//*[@class="a-unordered-list a-horizontal a-size-small"]/li[9]/span/a/text()').get()

        
        if l1==None or l1==product_name:
            l1=None
        if l2==None or l2==product_name:
            l2=None
        if l3==None or l3==product_name:
            l3=None
        if l4==None or l4==product_name:
            l4=None
        if l5==None or l5==product_name:
            l5=None
        

        #image=response.xpath('//*[@id="landingImage"]/@data-a-dynamic-image').get()
        ''' if image is None :
            filet=open('failed.txt','a')
            filet.write(str(response.url)+"\n")

        img=str(image).split(':')
        image_url="https:"+str(img[1])
        
        image_url=image_url.replace('"','')'''
       
        seling=response.xpath('//*[@class="a-offscreen"]/text()').get()
        if seling is not None:
            seling=seling.replace('\u20b9', '')
        mrp_amazon=response.xpath('//*[@class="a-section a-spacing-small aok-align-center"]/span/span/span/span/text()').get()
        if mrp_amazon is not None:
            mrp_amazon=mrp_amazon.replace('\u20b9', '')
        print(mrp_amazon)
        print(seling)

        stock=response.xpath('//*[@id="availability"]/span/text()').get()
        print(stock)

        brand_name=''
        brand=response.xpath('//*[@id="bylineInfo_feature_div"]/div/a/text()').get()
        if brand is not None :
            brand_nm=brand.split(":")
            print(brand_nm)
            if "Brand" in brand_nm:
                brand_name=brand_nm[1]
            else :
                brand_name=None
        #print about this item
        key_items=response.xpath('//*[@id="feature-bullets"]/ul/li').getall()
        abt_items=''
        for k in range(1,len(key_items)+1):
          item_index=str(k)
          abt_items=abt_items+str(response.xpath('//*[@id="feature-bullets"]/ul/li['+item_index+']/span/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b')+ " || "
          #print(abt_items)

        #print(brand_name)
        tab=response.xpath('//*[@id="product-specification-table"]/tr').getall()
        #print(len(tab))

        table=response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr').getall()
        #print(len(table))
        tablecc=response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr[1]/th/text()').get()
        #print(tablecc)
        #create tuple
        technical_details={}
        #print technical details
        table_data=''
        if len(table) !=0 :
            for i in range(1,len(table)+1) :
                indx=str(i)
                table_data=table_data+str(response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr['+indx+']/th/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b')+" : "+str(response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr['+indx+']/td/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b').strip()+" || "
                #creating the data structure as key value pair for manufacture product detail country or origin
                prefix_key=str(response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr['+indx+']/th/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b')
                prefix_key=re.sub("'",'',prefix_key).strip('')
                suffix_value=str(response.xpath('//*[@id="productDetails_techSpec_section_1"]/tr['+indx+']/td/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b').strip()
                suffix_value=suffix_value.split('x8e')[1]
                suffix_value=re.sub("'",'',suffix_value).strip('')
                #print("prefix key :" +prefix_key + " : "+"suffix_value " +suffix_value)
                technical_details[prefix_key]=suffix_value
        key=response.xpath('//*[@id="feature-bullets"]/ul')
        key_range=response.xpath('//*[@id="feature-bullets"]/ul/li').getall()
        key_features=''
        for j in range(1,len(key_range)+1): 
            index=str(j)
            key_features=key_features+str(response.xpath('//*[@id="feature-bullets"]/ul/li['+index+']/span/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b').strip()+" || "

        
        #print additional info
        additional_data={}
        lst=['ASIN','Best Sellers Rank','Date First Available','Manufacturer','Packer','Generic Name','Customer Reviews','Manufacturer Series Number','EAN','Part Number','UPC']
        add=''
        add_info=response.xpath('//*[@id="productDetails_detailBullets_sections1"]/tr')
        for k in add_info :
            name=k.xpath('th/text()').get()
            if name is not None :
                name=str(name.encode("utf-8")).strip('\n').strip().strip('b')
            if name not in lst :
                add=add+str(name)+":"+str(k.xpath('td/text()').get().encode('utf-8')).strip('\n').strip().strip('b')+" || "
                pre_key=re.sub("'",'',str(name)).strip('')
                suf_value=re.sub("'",'',str(k.xpath('td/text()').get().encode('utf-8')).strip('\n').strip().strip('b'))
                additional_data[pre_key]=suf_value
        #print(add)



        #print product other details info 
        table_o=response.xpath('//*[@class="a-normal a-spacing-micro"]/tr').getall()
        product_o_details=''
        if len(table_o) !=0 :
            for i in range(1,len(table_o)+1) :
                indx=str(i)
                product_o_details=product_o_details+str(response.xpath('//*[@class="a-normal a-spacing-micro"]/tr['+indx+']/td/span/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b')+" : "+str(response.xpath('//*[@class="a-normal a-spacing-micro"]/tr['+indx+']/td[@class="a-span9"]/span/text()').get().encode('utf-8')).strip('\n').strip('\t').strip('b').strip()+" || "

        #print(product_o_details)
       
        images=[]
        img=response.xpath('//*[@id="altImages"]/ul/li[@class="a-spacing-small item"]/span/span/span/span/span/img/@src').getall()
        for i in img:
            im=str(i).split("._")
            i=im[0]+"._S400_.jpg"
            images.append(i)
            #print(i)
        if len(images)==0 :
            filet=open('failed_netmart.txt','a')
            filet.write(str(response.url)+"\n")

         
        #print product specification table
        tab=response.xpath("//*[@id='product-specification-table']/tr").getall()
        tab_data=""
        k=1
        if len(tab) !=0 :
            while k<len(tab) :
                j=str(k)
                left=response.xpath('//*[@id="product-specification-table"]/tr['+j+']/th/text()').get()
                left=str(left).strip('\n')
                #print(left)
                if left!="None":
            
                    if left not in lst :
                        tab_data=tab_data+str(left.encode('utf-8')).strip('b')+":"+str(response.xpath('//*[@id="product-specification-table"]/tr['+j+']/td/text()').get().encode('utf-8')).strip('\n').strip('b').strip()+" || "
                k=k+1
        #print(tab_data)

        #print product details
        lstP=['Is Discontinued By Manufacturer','Product Dimensions','Date First Available','Manufacturer','ASIN','Item model number','Country of Origin','Packer','Importer','Item Weight','Item Dimensions LxWxH','Net Quantity','Included Components'] 
        lstdata=response.xpath('//*[@id="detailBullets_feature_div"]/ul/li').getall()
        datalst={}
        dt=""
        pD=""
        im=""
        daf=""
        man=""
        asin=""
        imn=""
        coo=""
        packer=""
        impo=""
        iw=""
        id=""
        nq=""
        ic=""
        for i in range(1,len(lstdata)+1) :
            i=str(i)
            left=response.xpath('//*[@id="detailBullets_feature_div"]/ul/li['+i+']/span/span[1]/text()').get()
            right=response.xpath('//*[@id="detailBullets_feature_div"]/ul/li['+i+']/span/span[2]/text()').get()
            datalst[left]=right

        for i in datalst.keys() :
            if(i.startswith(tuple(lstP))==True) :
                #print( "i :"+i)
                if( "Is Discontinued By Manufacture" in i):
                    im=datalst.get(i).strip('')
                if("Product Dimension" in i):
                    pD=re.sub(";",'',datalst.get(i).strip(''))
                if("Date First Available" in i):
                    daf=datalst.get(i).strip('')
                if("Manufacturer" in i):
                    man=datalst.get(i).strip('')
                if("ASIN" in i):
                    asin=datalst.get(i).strip('')
                if("Item model number" in i):
                    imn=datalst.get(i).strip('')
                if("Country of Origin" in i):
                    coo=datalst.get(i).strip('')
                if("Packer" in i):
                    packer=datalst.get(i).strip('')
                if( "Importer" in i):
                    impo=datalst.get(i).strip('')
                if("Item Weight" in i):
                    iw=datalst.get(i).strip('')
                if("Item Dimensions LxWxH" in i):
                    id=datalst.get(i).strip('')
                if("Net Quantity" in i):
                    nq=datalst.get(i).strip('')
                if("Included Components" in i):
                    ic=datalst.get(i).strip('')
                
                #print(datalst.get(i).strip('').strip(':'))
                dt=dt+i+datalst.get(i)+"||"
        #print(dt)

        #capture the brandName if it is not scrapped
        if brand_name is None:
            if product_o_details!="None":
               brand_name=product_o_details.split("||",1)[0]
               if(len(brand_name.strip())) :
                  brand_name=brand_name.split(":")[1]
            print(brand_name)  

        #add manufacture and other info if product details is null
        #print(len(lstdata))
        if(len(lstdata)==0):
            for i in technical_details.keys() :
             if("Product Dimension" in i):
                    pD=re.sub(";",'',technical_details.get(i).strip(''))
             if("Date First Available" in i):
                    daf=technical_details.get(i).strip('')
             if(len(man)==0):
                if("Manufacturer" in i):
                    man=technical_details.get(i).strip('')
                else:
                 if("Manufacturer" in i):
                    man=technical_details.get(i).strip('')
             if(len(asin)==0):
                if("ASIN" in i):
                    asin=technical_details.get(i).strip('')
                else:
                 if("ASIN" in i):
                    asin=technical_details.get(i).strip('')

             if("Item model number" in i):
                    imn=technical_details.get(i).strip('')
             if("Country of Origin" in i):
                    coo=technical_details.get(i).strip('')
             if(len(iw)==0):
                if("Item Weight" in i):
                    iw=technical_details.get(i).strip('')
                else:
                 if("Item Weight" in i):
                    iw=technical_details.get(i).strip('')
             
             

            for k in additional_data.keys():
                if("Packer" in k):
                    packer=additional_data.get(k).strip('')
                if( "Importer" in k):
                    impo=additional_data.get(k).strip('')
                if("Item Dimensions LxWxH" in k):
                    id=additional_data.get(k).strip('')
                
                if(len(asin)==0):
                 if("ASIN" in k):
                    asin=additional_data.get(k).strip('')
                 else:
                  if("ASIN" in k):
                    asin=additional_data.get(k).strip('')

                if("Net Quantity" in k):
                    nq=additional_data.get(k).strip('')
                if("Included Components" in k):
                    ic=additional_data.get(k).strip('')
                if(len(iw)==0):
                 if("Item Weight" in k):
                    iw=additional_data.get(k).strip('')
                 else:
                  if("Item Weight" in k):
                    iw=additional_data.get(k).strip('')   
                if("Date First Available" in k):
                    daf=additional_data.get(k).strip('')
                             
                
       
        
        #table_data=table_data+dt
        data={
            'Product_Name':product_name,
            'Url':response.url,
            'Technical_Details': table_data,
            'Specification':product_o_details,
            'Mrp_Amazon':mrp_amazon,
            'SP_Amazon':seling,
            'Stock_status':stock,
            'Category_L1':l1,
            'Category_L2':l2,
            'Category_L3':l3,
            'Category_L4':l4,
            'Category_L5':l5,
            'Brand_name':brand_name,
            'image':images,
            'About_this_Items':abt_items,
            'Additional_Details':add,
            'Product_Specification':tab_data,
            'Product_details':dt,
            'Is Discontinued By Manufacturer':im,
            'Product Dimension':pD,
            'Date First Available':daf,
            'Manufacturer':man,
            'ASIN':asin,
            'Item model number':imn,
            'Country of Origin':coo,
            'Packer':packer,
            'Importer':impo,
            'Item Weight':iw,
            'Item Dimensions LxWxH':id,
            'Net Quantity':nq,
            'Included Components':ic

        }
        
        yield data
