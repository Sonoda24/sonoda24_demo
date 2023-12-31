# -*- coding: utf-8 -*-
"""
Created on Sat May 30 10:17:22 2020

@author: user
"""
# Create your views here.
from django.http import HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, redirect

from db_serv.forms import My_ImageForm
from db_serv.models import My_Image

from db_serv.forms import UploadFileForm
from db_serv.models import My_Data
from db_serv.models import My_Svg
from db_serv.models import My_CnSvg
from db_serv.models import My_Sys
from db_serv.models import My_Index
from db_serv.models import My_Recs
from db_serv.models import My_Script
#from db_serv.models import Reg_Svg
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest, JsonResponse

import os, csv
import sys
import re
import random
import inspect
#from six import unichr
#from six.moves.html_entities import codepoint2name, name2codepoint
from html.entities import codepoint2name, entitydefs, name2codepoint
import codecs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.views import generic
from django.conf import settings
from django.core.files.storage import default_storage
from django.views import generic
from django.core import serializers

from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

db_data=''
svg_data=''
l0_keys=['']
l0_nums=[0]
l0_nn=[1]
l1_keys=['']
l1_nums=[0]
l1_nn=[1]
l2_keys=['']
l2_nums=[0]
l2_nn=[1]
l3_keys=['']
l3_nums=[0]
l3_nn=[1]
recs_nums=[]

recs_data=''
ixdata_3=''
ixdata_2=''
ixdata_1=''
ixdata_0=''
ixdata=''

pk_l0=0
pk_l1=0
pk_l2=0
pk_l3=0
pk_recs=0
#first_run=1
mydata_org=[]
#mydata_list=[]
mydata=[]

Srch_level=0
Srch_prev_level=0
Srch_key=''
Srch_prev_key=''
Srch_v0_pkn=0
Srch_v0_key=''
Srch_v1_pkn=0
Srch_v1_key=''
Srch_v2_pkn=0
Srch_v2_key=''
Srch_v3_pkn=0
Srch_v3_key=''

Stage_ind=0
mod_keys=[]
mod_nums=[]
mod_nn=[]
index_delstack=[]
paginatorr=''

parm_len=0
sfield=''

g_upload_fg=0
g_pk_num=0
g_my_sys_num=0
g_my_data_num=0
g_my_svg_num=0
g_my_cnsvg_num=0
my_oldno=0
my_olddfg=0
myold_cnsvgtags=''
old_cnsvg_nums=0

st_step=''
nn_list=[]
n_sys_tot=0
n_sys=0
n_docs=0
n_docs_tot=0
ex_cnsvg=''
n_cnsvg_tot=0
nn_cnsvg=0
after_next=''

# ------------------------------------------------------------------   
class My_ImageList(generic.ListView):
    model = My_Image
    paginate_by = 6
    template_name = 'db_serv/image_down.html'

# ------------------------------------------------------------------    
def get_mylist(request):
    #print('***get_mylist')

    #my_image_list = My_Image.objects.all()
    my_image_list = My_Image.objects.all().order_by('uploaded_at').reverse()
    #print('**all obj=',my_image_list)

    page_obj = paginate_queryset(request, my_image_list, 6)
    #print('**page obj=',type(page_obj),len(page_obj),page_obj.object_list)
    
    context = {
        'page_list': page_obj.object_list,
        'page_obj': page_obj,
    }
    
    return render(request, 'db_serv/image_down2.html',context)
# ------------------------------------------------------------------ 
def get_mylist2(request):
    #print('***get_mylist2')

    my_image_list = My_Image.objects.all()
    #print('**all obj=',my_image_list)

    page_obj = paginate_queryset(request, my_image_list, 6)
    #print('**page obj=',type(page_obj),len(page_obj),page_obj.object_list)
    
    context = {
        'page_list': page_obj.object_list,
        'page_obj': page_obj,
    }
    return JsonResponse(context)
    #return render(request, 'db_serv/editor.html', context)
# ------------------------------------------------------------------    
def get_testchar(request):
    #print('**get_testchar')
    tex = request.GET.get("testchar")
    #print('testchar=',tex)
    context={'my_editor_var':tex}
    #return render(request, 'db_serv/editor.html',context)
    return JsonResponse(context)
# ------------------------------------------------------------------
def imagedownload(request):
    print('ImageDownload Get/Post=',request.POST,' FILES=',request.FILES)
    file_pks = request.POST.getlist('pick')  # <input type="checkbox" name="zip"のnameに対応
    #print('picked pks=',file_pks)
    if(len(file_pks)>0):
        image_files = My_Image.objects.filter(pk__in=file_pks)
        image=image_files[0]
        #print('image=',image,image.photo)
        context = {
            'url': image.photo.url,
            'function_name': 'after_close_pop',
            }
    else:
        context = {
            'url': 'error',
            'function_name': 'after_close_pop',
            }
        
    return render(request, 'db_serv/close_pop.html',context)
    #return JsonResponse(response)
# ------------------------------------------------------------------
def imageupload(request):
    #My_Imagelist = My_Image.objects.all()
    #print('ImageUpload Get/Post=',request.POST,' FILES=',request.FILES)
    if request.method == 'POST':
        form = My_ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img=form.save()
            #print('**Upload Image=',img)
            url=img.photo.url
            return JsonResponse({'url': url})
            #return
# ------------------------------------------------------------------
def index(request):
    #print('*****server started')
    context = {}
    return render(request,'db_serv/index.html',context)
# ------------------------------------------------------------------
def set_shipment(request):
    print('*****set_shipment started')
    context = {}
    return render(request,'db_serv/set_shipment.html',context)
# ------------------------------------------------------------------
def nlist(request):
    #model recordの一覧を調べる
    #list = My_Data.objects.all().order_by('no')
    #print('My_Data record numbers=',list.length)
    list = My_Recs.objects.all().order_by('no')
    #print('My_Recs record numbers=',len(list))
    for data in list:
        print('number=',data.no,'kind=',data.kind)
        
    return HttpResponse('complete!')
# -----------------------------------------------------------------
def new_list(request):
    print('@@@@Enter this rout')
    return render(request, 'db_serv/new_list.html',{})
# -----------------------------------------------------------------
def new_list_parms(request,keys):
#    new_list_new called http://127.0.0.1:8000/new_list_parms/My_Note,使用説明
#    parms = request.GET.get('parms', None)
    global parm_len
    global sfield
    
    print('Enter new_list_parms keys=',keys)
    
    if(keys=='none'):
        parm_len=0
        sfield=''
    else:
        parms=keys.split(',')
        #print('parms=',keys,parms)
        #print('parms=',keys,parms,'leng=',len(parms))
        if(keys=="My_Note,使用説明"):
            parm_len=len(parms)
            sfield=["theme","bunrui1","bunrui2","bunrui3"][parm_len]
        else:
            #print('new_list_parms and parm_len=',parm_len,'keys=',keys)
            parm_len=0
            
            
    #print('Enter new_list_parms and parm_len=',parm_len,'sort field=',sfield)
    
    return render(request, 'db_serv/new_list.html',{'parm_keys':keys})
# -----------------------------------------------------------------
def get_new_list_first(request):
    #global first_run
    global mydata_org
    global mydata_list
    global mydata
    global paginatorr
    
    global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0
    
    global Srch_level
    global Srch_prev_level
    global Srch_key
    global Srch_prev_key
    global Srch_v0_pkn
    global Srch_v0_key
    global Srch_v1_pkn
    global Srch_v1_key
    global Srch_v2_pkn
    global Srch_v2_key
    global Srch_v3_pkn
    global Srch_v3_key
    
    global parm_len
    global sfield
    
    parm_len=2
    sfield=["theme","bunrui1","bunrui2","bunrui3"][parm_len]
    level = request.GET.get('level', None)
    page = request.GET.get('page', None)
    parms = request.GET.get('parms', None)
    
    pk_nums=[]
    page_ns=[]
    key_wds=[]
    terms=parms.split(';')
    #print('parms=',parms,'terms=',terms);
    for k in range(5):
        parm=terms[k].split(',')
        #print('parm=',parm)
        pk_nums.append(parm[0])
        page_ns.append(parm[1])
        key_wds.append(parm[2])

    dmylevel,rec_num,key_nums,key_tags=get_index_sub(level,pk_nums[int(level)])
    #print('Get index rec_num=',rec_num,key_nums,key_tags)

    """
    page_n = request.GET.get('page_n', None) #getting page number    
    level = request.GET.get('level',None)
    pk_num = request.GET.get("pk_num",None)
    key_wd= request.GET.get("key_wd",None)
    info('**At Top  level=' +str(level)+' pk_num='+str(pk_num)+' key_wd='+key_wd+' page_n='+str(page_n))
    """
    
    if(len(mydata_org)==0):
        #mydata_list = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all().order_by("day_regist").reverse()
        mydata_org = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").exclude(dfg=True).order_by("day_regist").reverse()
        #level="0"
        #mydata_list = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").exclude(dfg=True).order_by("day_regist").reverse()
        mydata_org=mydata_org.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview")
        #print('my_data_list at new_list 1st startpoint leng=',len(mydata_list))
        #first_run=0
        mydata=mydata_org

        #info("***Init orglist leng="+str(len(mydata_org)))
        #parm_len=0
        #debug("my_data_list at new_list 1st startpoint")
        Srch_prev_level=4
        Srch_prev_key=''
        
    #present_level=int(level)
    key=key_wds[int(Srch_level)]
    if(page=='0'):
        page_n=1
    else:
        page_n=int(page)

    if(page=='0'):
        sel_mydata=extract_list(level,key,key_wds)
    else:
        sel_mydata=mydata

    context = {
        'level':level,
        'key_nums':key_nums,
        'key_tags':key_tags,
        }
    return JsonResponse(context)
    #return render(request, 'db_serv/new_list.html',context)
# -----------------------------------------------------------------
def get_new_list(request):
    #global first_run
    global mydata_org
    global mydata_list
    global mydata
    global paginatorr
    
    global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0
    
    global Srch_level
    global Srch_prev_level
    global Srch_key
    global Srch_prev_key
    global Srch_v0_pkn
    global Srch_v0_key
    global Srch_v1_pkn
    global Srch_v1_key
    global Srch_v2_pkn
    global Srch_v2_key
    global Srch_v3_pkn
    global Srch_v3_key
    
    global parm_len
    global sfield
    
    #level = request.GET.get('level', None)
    #page = request.GET.get('page', None)
    #parms = request.GET.get('parms', None)
    level = request.POST.get('level', None)
    page = request.POST.get('page', None)
    parms = request.POST.get('parms', None)
    
    #print('Enter get_new_list and parm_len=',parm_len,'page=',page)
    
    p_level='0'
    if(level=='99'):
        #print('level 99 catch level=',level)
        p_level='99'
        level='0'
    
    pk_nums=[]
    page_ns=[]
    key_wds=[]
    terms=parms.split(';')
    #print('parms=',parms,'terms=',terms);
    for k in range(5):
        parm=terms[k].split(',')
        #print('parm=',parm)
        pk_nums.append(parm[0])
        page_ns.append(parm[1])
        key_wds.append(parm[2])
        
    dmylevel,rec_num,key_nums,key_tags=get_index_sub(level,pk_nums[int(level)])
    #print('Get index rec_num=',rec_num,key_nums,key_tags)

    """
    page_n = request.GET.get('page_n', None) #getting page number    
    level = request.GET.get('level',None)
    pk_num = request.GET.get("pk_num",None)
    key_wd= request.GET.get("key_wd",None)
    info('**At Top  level=' +str(level)+' pk_num='+str(pk_num)+' key_wd='+key_wd+' page_n='+str(page_n))
    """
    
    if(len(mydata_org)==0):
        #mydata_list = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all().order_by("day_regist").reverse()
        mydata_org = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").exclude(dfg=True).order_by("day_regist").reverse()
        #level="0"
        #mydata_list = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").exclude(dfg=True).order_by("day_regist").reverse()
        #mydata_org=mydata_org.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").order_by("day_regist").reverse()
        mydata_org=mydata_org.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview")
        mydata=mydata_org
        
        #print('my_data_list at new_list 1st startpoint leng=',len(mydata_list))
        #first_run=0
        #info("***Init orglist leng="+str(len(mydata_org)))
        #debug("my_data_list at new_list 1st startpoint")
        Srch_prev_level=4
        Srch_prev_key=''
    #present_level=int(level)
    key=key_wds[int(Srch_level)]
    if(page=='0'):
        page_n=1
    else:
        page_n=int(page)

    if(page=='0'):
        sel_mydata=extract_list(level,key,key_wds)
    else:
        sel_mydata=mydata
        
    if(parm_len):
        param1="'-"+sfield+"'"
        param2="'"+'day_regist'+"'"
        param=param1+','+param2
        #print('order_by=',param,param1,param2)
        sel_mydata=sel_mydata.order_by('-bunrui2','day_regist')
        #sel_mydata=sel_mydata.order_by(param1,param2)
        #sel_mydata=sel_mydata.order_by(param)
        #sel_mydata=sel_mydata.order_by(sfield).reverse()
        parm_len=0

    #print('After Select mydata leng=',len(mydata),'mydata_list leng=',len(mydata_list))
    mess=" key="+key+" len="+str(len(sel_mydata))
    #info("After:level="+str(level)+mess)
    mydata_b=sel_mydata.values()
    paginatorr = Paginator(mydata_b, 20)
    #import inspect
    #print('paginator=',inspect.getmembers(paginatorr.page))

    try:
        result = paginatorr.page(page_n).object_list
    except PageNotAnInteger:
        result = paginatorr.page(1).object_list
    except EmptyPage:
        result = paginatorr.page(1).object_list

        #results=list(paginatorr.page(page_n).object_list)
        #results = list(paginatorr.page(page_n))
    results=list(result)
    page_range = paginatorr.page_range
    prange=list(page_range)
    context = {
        'level':level,
        'key_nums':key_nums,
        'key_tags':key_tags,
        'page_n':str(page_n),
        'results':results,
        'page_range':prange,
        }
    return JsonResponse(context)
    #return render(request, 'db_serv/new_list.html',context)
# -----------------------------------------------------------------
def after_key_change(request):
    #global first_run
    global mydata_org
    global mydata_list
    global mydata
    global paginatorr
    
    global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0
    
    global Srch_level
    global Srch_prev_level
    global Srch_key
    global Srch_prev_key
    global Srch_v0_pkn
    global Srch_v0_key
    global Srch_v1_pkn
    global Srch_v1_key
    global Srch_v2_pkn
    global Srch_v2_key
    global Srch_v3_pkn
    global Srch_v3_key
    
    global parm_len
    global sfield
    
    #level = request.GET.get('level', None)
    #page = request.GET.get('page', None)
    #parms = request.GET.get('parms', None)
    level = request.POST.get('level', None)
    parms = request.POST.get('parms', None)
    
    pk_nums=[]
    key_wds=[]
    terms=parms.split(';')
    #print('parms=',parms,'terms=',terms);
    for k in range(6):
        parm=terms[k].split(',')
        #print('parm=',parm)
        pk_nums.append(parm[0])
        key_wds.append(parm[2])
 
    for data in mydata:
        data_id=data.no
        db = My_Data.objects.get(pk=data_id)
        if(level=='1'):
            if(db.theme==key_wds[1]):
                db.theme=key_wds[5]
        elif(level=='2'):
            if(db.bunrui1==key_wds[2]):
                db.bunrui1=key_wds[5]           
            
        elif(level=='3'):
            if(db.bunrui2==key_wds[3]):
                db.bunrui2=key_wds[5]           
            
        elif(level=='4'):
            if(db.bunrui3==key_wds[4]):
                db.bunrui3=key_wds[5]     
        #print('dat=',db.theme,db.bunrui1,db.bunrui2,db.bunrui3)
        db.save()

    recn=str(len(mydata))
    context = {
        'level':level,
        'leng':recn,
        }
    return JsonResponse(context)
    #return render(request, 'db_serv/new_list.html',context)
# -----------------------------------------------------------------
def get_new_page(request):
    global paginatorr
    
    page = request.GET.get('page', None) #getting page number    
    page_n=int(page)
    
    try:
        result = paginatorr.page(page_n).object_list
    except PageNotAnInteger:
        result = paginatorr.page(1).object_list
    except EmptyPage:
        result = paginatorr.page(1).object_list

        #results=list(paginatorr.page(page_n).object_list)
        #results = list(paginatorr.page(page_n))
    results=list(result)
    page_range = paginatorr.page_range
    prange=list(page_range)
    context = {
        'page_n':str(page_n),
        'results':results,
        'page_range':prange,
        }
    return JsonResponse(context)
    #return render(request, 'db_serv/new_list.html',context)
# -----------------------------------------------------------------
def extract_list(level,key,key_wds):
    global mydata_org
    global mydata_list
    global mydata
    
    global Srch_level
    global Srch_prev_level
    global Srch_key
    global Srch_prev_key
    global Srch_v0_pkn
    global Srch_v0_key
    global Srch_v1_pkn
    global Srch_v1_key
    global Srch_v2_pkn
    global Srch_v2_key
    global Srch_v3_pkn
    global Srch_v3_key
    
    Srch_level=int(level)
    Srch_key=key
    if (Srch_level>Srch_prev_level):
        mydata_list=mydata
        #info("StepA list leng="+str(len(mydata_list)))
        if Srch_level==1:
            #print('Search level=theme key_wd=',Srch_v0_key)
            Srch_v0_key=Srch_key
            #info("Theme:"+Srch_v0_key)
            #debug("Search level=theme")
            mydata=mydata_list.filter(theme=Srch_v0_key)
            Srch_prev_level=Srch_level

        if Srch_level==2:
            Srch_v1_key=Srch_key
            mydata=mydata_list.filter(bunrui1=Srch_v1_key)
            Srch_prev_level=Srch_level
            #info("Bunrui1:"+Srch_v1_key)
            #debug("Search level=bunrui1")
            #print('Search level=bunrui1 key_wd=',Srch_v1_key)

        if Srch_level==3:
            Srch_v2_key=Srch_key
            mydata=mydata_list.filter(bunrui2=Srch_v2_key)
            Srch_prev_level=Srch_level
            #info("Bunrui2:"+Srch_v2_key)
            #debug("Search level=bunrui2")
            #print('Search level=bunrui2 key_wd=',Srch_v2_key)

        if Srch_level==4:
            Srch_v3_key=Srch_key
            mydata=mydata_list.filter(bunrui3=Srch_v3_key)
            Srch_prev_level=Srch_level
            #info("Bunrui3:"+Srch_v3_key)
            #debug("Search level=bunrui3")
            #print('Search level=bunrui3 key_wd=',Srch_v3_key)

        #print('mydata leng=',len(mydata_list))
        sel_mydata=mydata

    elif Srch_level<Srch_prev_level:
        #mydata_list = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").exclude(dfg=True).order_by("day_regist").reverse()
        #mydata_list=mydata_list.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview")
        Srch_prev_key=""
        mydata=mydata_org
        mydata_list=mydata_org
        #info("StepB list leng="+str(len(mydata)))
        #print('my_data_list at new_list 2nd startpoint leng=',len(mydata_list))

        if Srch_level>=1:
            Srch_v0_key=key_wds[1]
            mydata_list=mydata
            mydata=mydata_list.filter(theme=Srch_v0_key)
            #info("new Theme:"+Srch_v0_key)
            #print('new Search level=theme key_wd=',Srch_v0_key)
        if Srch_level>=2:
            Srch_v1_key=key_wds[2]
            mydata_list=mydata
            mydata=mydata_list.filter(bunrui1=Srch_v1_key)
            #info("new Bunrui1:"+Srch_v1_key)
            #print('new Search level=bunrui1 key_wd=',Srch_v1_key)
        if Srch_level>=3:
            Srch_v2_key=key_wds[3]
            mydata_list=mydata
            mydata=mydata_list.filter(bunrui2=Srch_v2_key)
            #info("new Bunrui2:"+Srch_v2_key)
            #print('new Search level=bunrui2 key_wd=',Srch_v2_key)
        if Srch_level>=4:
            Srch_v3_key=key_wds[4]
            mydata_list=mydata
            mydata=mydata_list.filter(bunrui3=Srch_v3_key)
            #info("new Bunrui3:"+Srch_v2_key)
            #print('new Search level=bunrui3 key_wd=',Srch_v3_key)
        Srch_prev_level=Srch_level
        sel_mydata=mydata
        
    elif (Srch_key!=Srch_prev_key and Srch_prev_key!=''):
        #print('level=',Srch_level,' Srch_key=',Srch_key,' prev_key=',Srch_prev_key)
        #info("StepC list leng="+str(len(mydata_list)))
        if (Srch_level==1):
                Srch_v0_key=Srch_key
                mydata=mydata_list.filter(theme=Srch_v0_key)
        if (Srch_level==2):
                #print('key=',Srch_v1_key)
                Srch_v1_key=Srch_key
                mydata=mydata_list.filter(bunrui1=Srch_v1_key)
        if (Srch_level==3):
                #print('key=',Srch_v2_key)
                Srch_v2_key=Srch_key
                mydata=mydata_list.filter(bunrui2=Srch_v2_key)
        if (Srch_level==4):
                #print('key=',Srch_v3_key)
                Srch_v3_key=Srch_key
                mydata=mydata_list.filter(bunrui3=Srch_v3_key)
        sel_mydata=mydata
        Srch_prev_key=Srch_key
    else:
        sel_mydata=mydata
        #info("Start list leng="+str(len(mydata)))
        
    return sel_mydata
# -----------------------------------------------------------------
def new_list_shipment(request):
    global first_run
    global mydata_list
    global mydata
    
    global Srch_level
    global Srch_prev_level
    global Srch_key
    global Srch_prev_key
    global Srch_v0_pkn
    global Srch_v0_key
    global Srch_v1_pkn
    global Srch_v1_key
    global Srch_v2_pkn
    global Srch_v2_key
    global Srch_v3_pkn
    global Srch_v3_key
    
    #mydata_list = My_Data.objects.values("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all()
    #print('my_data_list leng=',len(mydata_list))
    
    if first_run==1:
        mydata_list = My_Data.objects.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all().order_by("day_regist").reverse()
        #print('my_data_list at new_list startpoint leng=',len(mydata_list))
        first_run=0
    
    #print('Search level check Level=',Srch_level,' prev=',Srch_prev_level)
    if (Srch_level>Srch_prev_level):
        mydata_list=mydata
        if Srch_level==1:
            #print('Search level=theme key_wd=',Srch_v0_key)
            mydata=mydata_list.filter(theme=Srch_v0_key)
            Srch_prev_level=Srch_level

        if Srch_level==2:
            mydata=mydata_list.filter(bunrui1=Srch_v1_key)
            Srch_prev_level=Srch_level
            #print('Search level=bunrui1 key_wd=',Srch_v1_key)

        if Srch_level==3:
            mydata=mydata_list.filter(bunrui2=Srch_v2_key)
            Srch_prev_level=Srch_level
            #print('Search level=bunrui2 key_wd=',Srch_v2_key)

        if Srch_level==4:
            mydata=mydata_list.filter(bunrui3=Srch_v3_key)
            Srch_prev_level=Srch_level
            #print('Search level=bunrui3 key_wd=',Srch_v3_key)

        #print('mydata leng=',len(mydata_list))

    elif Srch_level<Srch_prev_level:
        mydata_list = My_Data.objects.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all().order_by("day_regist").reverse()
        mydata=mydata_list
        #print('my_data_list at new_list startpoint leng=',len(mydata_list))

        if Srch_level>0:
            mydata_list=mydata
            mydata=mydata_list.filter(theme=Srch_v0_key)
            #print('new Search level=theme key_wd=',Srch_v0_key)
        if Srch_level>1:
            mydata_list=mydata
            mydata=mydata_list.filter(bunrui1=Srch_v1_key)
            #print('new Search level=bunrui1 key_wd=',Srch_v1_key)
        if Srch_level>2:
            mydata_list=mydata
            mydata=mydata_list.filter(bunrui2=Srch_v2_key)
            #print('new Search level=bunrui2 key_wd=',Srch_v2_key)
        if Srch_level>3:
            mydata_list=mydata
            mydata=mydata_list.filter(bunrui3=Srch_v3_key)
            #print('new Search level=bunrui3 key_wd=',Srch_v3_key)
        Srch_prev_level=Srch_level
        
    elif (Srch_key!=Srch_prev_key):
        #print('level=',Srch_level,' Srch_key=',Srch_key,' prev_key=',Srch_prev_key)
        if (Srch_level==1):
            if (Srch_key=='課題名'):
                mydata=mydata_list
            else:
                #print('key=',Srch_v0_key)
                mydata=mydata_list.filter(theme=Srch_v0_key)
        if (Srch_level==2):
            if (Srch_key=='大分類'):
                mydata=mydata_list
            else:
                print('key=',Srch_v1_key)
                mydata=mydata_list.filter(bunrui1=Srch_v1_key)
        if (Srch_level==3):
            if (Srch_key=='中分類'):
                mydata=mydata_list
            else:
                #print('key=',Srch_v2_key)
                mydata=mydata_list.filter(bunrui2=Srch_v2_key)
        if (Srch_level==4):
            if (Srch_key=='小分類'):
                mydata=mydata_list
            else:
                #print('key=',Srch_v3_key)
                mydata=mydata_list.filter(bunrui3=Srch_v3_key)
    else:
        mydata=mydata_list

    #print('After Select mydata leng=',len(mydata),'mydata_list leng=',len(mydata_list))
    mydata_b=mydata.values()
    paginatorr = Paginator(mydata_b, 20)
    #import inspect
    #print('paginator=',inspect.getmembers(paginatorr.page))
    
    #
    if request.method == 'POST':
        page_n = request.POST.get('page_n', None) #getting page number
        #print('**POST page_n=',page_n)
        try:
            result = paginatorr.page(page_n).object_list
        except PageNotAnInteger:
            result = paginatorr.page(1).object_list
        except EmptyPage:
            result = paginatorr.page(1).object_list

        #results=list(paginatorr.page(page_n).object_list)
        #results = list(paginatorr.page(page_n))
        results=list(result)
        page_range = paginatorr.page_range
        prange=list(page_range)
        context = {
            'results':results,
            'page_range':prange,
            }
        return JsonResponse(context)
    
    #print('At First mydata leng=',len(mydata_list))
    #page_obj = paginate_queryset(request, mydata_list, 20)
    #page_obj = paginate_queryset(request, mydata, 20)
    #Paginator 
    #query_set for first page
    first_page = paginatorr.page(1).object_list
    #range of page ex range(1, 3)
    page_range = paginatorr.page_range
    #print('**page obj=',paginatorr,'first_page range=',first_page,page_range)
    
    context = {
        'first_page':first_page,
        'page_range':page_range
        }

    return render(request, 'db_serv/new_list_shipment.html',context)
# -----------------------------------------------------------------
def keyindex_change(request,keys):
#    new_list_new called http://127.0.0.1:8000/new_list_parms/My_Note,使用説明
#    parms = request.GET.get('parms', None)
    global parm_len
    global sfield
    
    if(keys=='none'):
        parm_len=0
        sfield=''
    else:
        parms=keys.split(',')
        #print('parms=',keys,parms)
        #print('parms=',keys,parms,'leng=',len(parms))
        parm_len=len(parms)
        sfield=["theme","bunrui1","bunrui2","bunrui3"][parm_len]
    #print('sort field=',sfield)
    
    return render(request, 'db_serv/keyindex_change.html',{'parm_keys':keys})
# -----------------------------------------------------------------
def pagenation(request):
    global first_run
    global mydata_list
    
    #mydata_list = My_Data.objects.values("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all()
    #print('my_data_list leng=',len(mydata_list))
    
    if first_run==1:
        mydata_list = My_Data.objects.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all().order_by("day_regist")
        #print('my_data_list at new_list startpoint leng=',len(mydata_list))
        first_run=0
    
    mydata=mydata_list.values()
    #print('mydata leng=',len(mydata))
    paginatorr = Paginator(mydata, 10)
    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range
    #print('**page obj=',paginatorr,'first_page range=',first_page,page_range)
    
    context = {
        'first_page':first_page,
        'page_range':page_range
        }
    #
    if request.method == 'POST':
        page_n = request.POST.get('page_n', None) #getting page number
        #print('**POST page_n=',page_n)
        results = list(paginatorr.page(page_n).object_list)
        prange=list(page_range)
        context = {
            'results':results,
            'page_range':prange
            }
        return JsonResponse(context)

    return render(request, 'db_serv/pagenation.html',context)
# ------------------------------------------------------------------    
def get_index_sub(level,pk_num):
    global mydata_org
    global mydata_list
    global mydata
    
    global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0
    
    global Srch_level
    global Srch_prev_level
    global Srch_key
    global Srch_prev_key
    global Srch_v0_pkn
    global Srch_v0_key
    global Srch_v1_pkn
    global Srch_v1_key
    global Srch_v2_pkn
    global Srch_v2_key
    global Srch_v3_pkn
    global Srch_v3_key

    #level = request.GET.get("level")
    #pk_num = request.GET.get("pk_num")
    #key_wd= request.GET.get("key_wd")
    #info('***Get_index_sub level='+level+' pk_num='+pk_num)
    Srch_prev_key=Srch_key
        
    if(level=='0'):
        #ixdata_0 = My_Index.objects.get(pk=1)
        ixdata_0 = My_Index.objects.get(pk=1)
        level=ixdata_0.level
        rec_num=ixdata_0.rec_num
        key_nums=ixdata_0.key_nums
        key_tags=ixdata_0.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v0_pkn=0
        Srch_v0_key=''
    
    if(level=='1'):
        ixdata_1 = My_Index.objects.get(pk=pk_num)
        level=ixdata_1.level
        rec_num=ixdata_1.rec_num
        key_nums=ixdata_1.key_nums
        key_tags=ixdata_1.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v0_pkn=pk_num
        
    if(level=='2'):
        ixdata_2 = My_Index.objects.get(pk=pk_num)
        level=ixdata_2.level
        rec_num=ixdata_2.rec_num
        key_nums=ixdata_2.key_nums
        key_tags=ixdata_2.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v1_pkn=pk_num
        
    if(level=='3'):
        ixdata_3 = My_Index.objects.get(pk=pk_num)
        level=ixdata_3.level
        rec_num=ixdata_3.rec_num
        key_nums=ixdata_3.key_nums
        key_tags=ixdata_3.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v2_pkn=pk_num
        
    if(level=='4'):
        level=4
        rec_num=0
        key_nums=0
        key_tags=''
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v3_pkn=0

    """
    context = {
        'level':level,
        'rec_num':rec_num,
        'key_nums':key_nums,
        'key_tags':key_tags,
    }
    """
    return level,rec_num,key_nums,key_tags
# ------------------------------------------------------------------
def mod_index(request):
    global ixdata
    global index_delstack
    global Stage_ind
    global mod_keys
    global mod_nums
    global mod_nn

    mod = request.GET.get("mod")
    level = request.GET.get("level")
    pk_num = request.GET.get("pk_num")
    key_wd= request.GET.get("key_wd")
    #print('***Mod_index Mod=',mod,'level=',level,'pk_num=',pk_num,'key_wd=',key_wd)
        
    if(mod=='start'):
        #print('mod start')
        if(level=='0'):
            Stage_ind=0
        elif(level=='1'):
            Stage_ind=1
        elif(level=='2'):
            Stage_ind=2
        elif(level=='3'):
            Stage_ind=3
        else:
            #print('modify key start stage error level=',level)
            return
        ixdata=My_Index.objects.get(pk=pk_num)
        mod_keys,mod_nums,mod_nn=tags_decompose(ixdata.key_tags)
        #print('mod_index stage=',Stage_ind,'nn=',mod_nn)
        Stage_ind+=1
    elif(mod=='last'):
        #print('Index Last Stage del record',index_delstack)
        if(len(index_delstack)>0):
            for k in range(len(index_delstack)):
                My_Index.objects.filter(pk=index_delstack[k]).delete()
                #print('del index=',index_delstack[k])
            index_delstack=[]
    else:
        if(Stage_ind>5):
            print('modify key stage error stage=',Stage_ind)
        npk_num=modify_index(mod,level,pk_num,key_wd)
        if(mod=='new'):
            ixdata.rec_num+=1
            ixdata.key_nums+=1
        #composeしてindexをsave（ixdataでlevel毎でなくてもOKか？）
        ixdata.key_tags=tags_compose(mod_keys,mod_nums,mod_nn)
        ixdata.save()
        if(Stage_ind<4):
            #print('modify stage=',Stage_ind)
            ixdata=My_Index.objects.get(pk=npk_num)
            mod_keys,mod_nums,mod_nn=tags_decompose(ixdata.key_tags)
        Stage_ind+=1

    #return JsonResponse(context)
    return HttpResponse('complete!')
# ------------------------------------------------------------------
def modify_index(mod,level,pk_num,key_wd):
    global index_delstack
    global mod_keys
    global mod_nums
    global mod_nn
    
    #print('mod comand=',mod,key_wd,mod_keys)
    k=-1
    for i in range(len(mod_nums)):
        #print('pk key=',pk_num,key_wd,mod_nums[i],mod_keys[i])
        if(int(pk_num)==mod_nums[i]):
            k=i
            #print('Search key=',key_wd,mod_keys[k])
            ret_num=mod_nums[k]
            break
    if((k>=0) and (mod=='add')):
        mod_nn[k]+=1
    elif((k>=0) and (mod=='del')):
        mod_nn[k]-=1
        if(mod_nn[k]<=0):
            index_delstack.append(mod_nums[k])
    elif((k<0) and (mod=='new')):
        ixobj=My_Index.objects.create()
        ixobj.no=ixobj.pk
        ixobj.kind='Ind'
        ixobj.level=level
        ixobj.mfg=False
        ixobj.rec_num=0
        ixobj.key_nums=0
        ixobj.key_tags=tags_compose([],[],[])
        ixobj.save()
        mod_keys.append(key_wd)
        mod_nums.append(ixobj.pk)
        mod_nn.append(int(1))
        ret_num=ixobj.pk
        #print('new key',mod_keys,mod_nums,mod_nn)
    else:
        print('Key index error detect')

    return ret_num
# ------------------------------------------------------------------
def make_index(request):
    
    My_Index.objects.all().delete()
    
    mydata_list = My_Data.objects.only("no","dfg","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").exclude(dfg=True).order_by("day_regist").reverse()
    pk_num=0
    ncnt=0
    pk_num=set_index(True,0,'','','','',pk_num)
            
    for my in mydata_list:
        ncnt=ncnt+1
        #print('***count=',ncnt,'data=',my.theme,my.bunrui1,my.bunrui2,my.bunrui3)
        pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,pk_num)
            
    all_save()
    #print('***make index My data count=',ncnt)

    return HttpResponse('complete!')
# ------------------------------------------------------------------
def resolve_index(request):
    #global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0

    ixdata_0 = My_Index.objects.get(pk=1)
    print('level=',ixdata_0.level,' rec_num=',ixdata_0.rec_num,' key_nums=',ixdata_0.key_nums)
    l0_keys,l0_nums,l0_nn=tags_decompose(ixdata_0.key_tags)
    l0=0
    print('l0_keys=',l0_keys,l0_nums,l0_nn)
    for l0_num in l0_nums:
        ixdata_1=My_Index.objects.get(pk=l0_num)
        print('   level=',ixdata_1.level,'key=',l0_keys[l0],' rec_num=',ixdata_1.rec_num,' key_nums=',ixdata_1.key_nums)
        l0=l0 +1
        l1_keys,l1_nums,l1_nn=tags_decompose(ixdata_1.key_tags)
        l1=0
        print('l1_keys=',l1_keys,l1_nums,l1_nn)
        for l1_num in l1_nums:
            ixdata_2=My_Index.objects.get(pk=l1_num)
            print('      level=',ixdata_2.level,'key=',l1_keys[l1],' rec_num=',ixdata_2.rec_num,' key_nums=',ixdata_2.key_nums)
            l1 = l1+1
            l2_keys,l2_nums,l2_nn=tags_decompose(ixdata_2.key_tags)
            l2=0
            print('l2_keys=',l2_keys,l2_nums,l2_nn)
            for l2_num in l2_nums:
                ixdata_3=My_Index.objects.get(pk=l2_num)
                level=ixdata_3.level
                rec_num=ixdata_3.rec_num
                key_nums=ixdata_3.key_nums
                key_tags=ixdata_3.key_tags
                print('         level=',ixdata_3.level,'key=',l2_keys[l2],' rec_num=',ixdata_3.rec_num,' key_nums=',ixdata_3.key_nums)
                l2=l2+1
                l3_keys,l3_nums,l3_nn=tags_decompose(ixdata_3.key_tags)
                l3=0
                print('l3_keys=',l3_keys,l3_nums,l3_nn)
                """
                for l3_num in l3_nums:
                    recs_data = My_Recs.objects.get(pk=l3_num)
                    recs_nums=recs_decompose(recs_data.tags)
                    print('            level=Recs numb=',recs_data.rec_num,'nums=',recs_nums)
                """
    return HttpResponse('resolved!')
# ------------------------------------------------------------------
def ai_image(request):
    #print('ai_image Get/Post=',request.POST,' FILES=',request.FILES)
    if request.method == 'POST':
        form = My_ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img=form.save()
            #print('**Upload Image=',img,img.photo.url)
            #return JsonResponse({'url': url})
            return redirect('showall')
            #return HttpResponse('complete!')
    else:
        #print('**ai_image Else')
        form = My_ImageForm()
        obj = My_Image.objects.all()
        #print(obj)
 
    return render(request, 'db_serv/model_form_upload.html', {
        'form': form,
        'obj': obj
    })    
# ------------------------------------------------------------------
def showall(request):
    images = My_Image.objects.all().order_by('uploaded_at').reverse()
    print("*** show all images")
    context = {'images':images}
    return render(request, 'db_serv/showall.html', context)
# ------------------------------------------------------------------
def download(request,data_id):
    image=My_Image.objects.get(pk=data_id)
    print("*** download one image")
    response = {'image':image}
    return response
# ------------------------------------------------------------------
###旧バージョン
def get_combo(request):
    tex = request.GET.get("message")
    print("**get_combo** recieve "+ tex);
    result = My_Data.objects.all().order_by('no')
    print('records = ',result.count())
    i=0
    for data in result:
        if(data.dfg==False):
            if(i==0):
                gMydbid=str(data.no)
                gComboA=data.theme
                gComboB=data.bunrui1
                gComboC=data.bunrui2
                gComboD=data.bunrui3
                gComboE=data.day_regist
                gComboF=data.overview
            else:
                #print(' record=',data.no,data.theme,data.overview)
                gMydbid=gMydbid+";,;"+str(data.no)
                gComboA=gComboA+";,;"+data.theme
                gComboB=gComboB+";,;"+data.bunrui1
                gComboC=gComboC+";,;"+data.bunrui2
                gComboD=gComboD+";,;"+data.bunrui3
                gComboE=gComboE+";,;"+data.day_regist
                gComboF=gComboF+";,;"+data.overview
            i=i+1

    context = {
	'no':gMydbid,
	'theme':gComboA,
	'bunrui1':gComboB,
	'bunrui2':gComboC,
	'bunrui3':gComboD,
	'day_regist':gComboE,
	'overview':gComboF,
        }
    print('** theme data **',gComboA);
    print('** bunrui3 data **',gComboD);

    return JsonResponse(context)
#    return HttpResponse(context)
#    return render(request, '',context)
#    return render(request, 'db_serv/get_combo.html',context)
# ------------------------------------------------------------------
def detail(request):
#def detail(request, data_id):
    """    
    global db_data,svg_data
    try:
        db_data = My_Data.objects.get(pk=data_id)
        view_tex=db_data.description
        print('Db_data',db_data.overview)
        svg_data=My_Svg.objects.get(pk=db_data.svg_no)
        svg_field=''
        if(svg_data.svg_tags!=''):
            svg_field = svg_data.svg_tags
            svg_field=svg_field.strip()
            print('**Svg=',svg_field)
        context = {
            'view_tex': view_tex,
            'svg_field': svg_field,
            }
    except My_Data.DoesNotExist:
        raise Http404("da_data does not exist")
    """
    context={}
    return render(request, 'db_serv/detail.html', context)
# ------------------------------------------------------------------    
def get_rec(request):
    global db_data,svg_data
    #print("**Start get_rec** recieve ")
    data_id = request.GET.get("rec_number")
    #print("rec_number= "+ data_id)
    db_data = My_Data.objects.get(pk=data_id)
    view_tex=db_data.description
    #print('***Db_data id= ',db_data.no,' svg_no= ',db_data.svg_no,' overview=',db_data.overview,'cnsvg_tags= ',db_data.cnsvg_tags)
    header=my_header(db_data.no,0,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
    overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
    svg_data=My_Svg.objects.get(pk=db_data.svg_no)
    svg_field=''
    if(svg_data.svg_tags!=''):
        svg_field = svg_data.svg_tags
        svg_field=svg_field.strip()
        #print('**Svg=',svg_field)
    context = {
        'header':header,
        'overviews':overviews,
        'view_tex': view_tex,
        'svg_field': svg_field,
        }    
    """
    data = My_Data.objects.get(pk=data_id)
    svg_data=My_Svg.objects.get(pk=data.svg_no)
    svg_field=''
    if(svg_data.svg_tags!=''):
        svg_field = svg_data.svg_tags
        svg_field=svg_field.strip()
    numb=str(data.no)
    theme=data.theme
    bunrui1=data.bunrui1
    bunrui2=data.bunrui2
    bunrui3=data.bunrui3
    day_regist=data.day_regist
    overview=data.overview
    description=data.description    
    
    context = {
	'no':numb,
	'theme':theme,
	'bunrui1':bunrui1,
	'bunrui2':bunrui2,
	'bunrui3':bunrui3,
	'day_regist':day_regist,
	'overview':overview,
        'view_tex':description,
        'svg_field':svg_field,
        }
    """
    return JsonResponse(context)
# ------------------------------------------------------------------    
def del_rec(request):
    global db_data,svg_data
    print("** Delete_record ** recieve ")
    data_id = request.GET.get("rec_number")
    print("rec_number= "+ data_id)
    db_data = My_Data.objects.get(pk=data_id)
    del_rec=db_data.no
    print('***Db_data id= ',db_data.no,' svg_no= ',db_data.svg_no,'cnnums=',db_data.cnsvg_nums,'cnsvg_tags= ',db_data.cnsvg_tags)
    svg_data=My_Svg.objects.get(pk=db_data.svg_no)
    db_data.dfg=True
    svg_data.dfg=True
    db_data.save()
    svg_data.save()
    """
    ln=db_data.cnsvg_nums
    if((ln!='') and (int(ln)>0)):
        tags=db_data.cnsvg_tags.split(';')
        #print('tabs=',tabs)
        for k in range(ln):
            nums=tags[k].split(',')
            print('num=',nums[1])
            cnsvg = My_CnSvg.objects.get(pk=nums[1])
            cnsvg.dfg=True
            cnsvg.save()
     """       
    context = {
        'del_rec':del_rec,
        }    

    return JsonResponse(context)
# ------------------------------------------------------------------
def editor(request,data_id):
    global db_data,svg_data
    try:
        if(data_id=='new'):
                header=''
                overviews=''
                view_tex=''
                svg_field=''
        else:
            db_data = My_Data.objects.get(pk=data_id)
            view_tex=db_data.description
            #print('***Db_data id= ',db_data.no,' svg_no= ',db_data.svg_no,' overview=',db_data.overview,'cnsvg_tags= ',db_data.cnsvg_tags)
            header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            #print('**header=',header)
            #print('overviews=',overviews)
            #overviews=''
            svg_data=My_Svg.objects.get(pk=db_data.svg_no)
            svg_field=''
            if(svg_data.svg_tags!=''):
                svg_field = svg_data.svg_tags
                svg_field=svg_field.strip()
                #print('**Svg=',svg_field)
        context = {
            'header':header,
            'overviews':overviews,
            'view_tex':view_tex,
            'svg_field':svg_field,
            }
    except My_Data.DoesNotExist:
        raise Http404("da_data does not exist")
    return render(request, 'db_serv/editor.html', context)
# ------------------------------------------------------------------
def editor_shipment(request,data_id):
    global db_data,svg_data
    try:
        db_data = My_Data.objects.get(pk=data_id)
        view_tex=db_data.description
        #print('***Db_data id= ',db_data.no,' svg_no= ',db_data.svg_no,' overview=',db_data.overview,'cnsvg_tags= ',db_data.cnsvg_tags)
        header=my_header(db_data.no,0,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
        overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
        svg_data=My_Svg.objects.get(pk=db_data.svg_no)
        svg_field=''
        if(svg_data.svg_tags!=''):
            svg_field = svg_data.svg_tags
            svg_field=svg_field.strip()
            #print('**Svg=',svg_field)
        context = {
            'header':header,
            'overviews':overviews,
            'view_tex': view_tex,
            'svg_field': svg_field,
            }
    except My_Data.DoesNotExist:
        raise Http404("da_data does not exist")
    return render(request, 'db_serv/editor_shipment.html', context)
# ------------------------------------------------------------------    
def my_header(no,kind,dfg,mfg,svg_no,cnsvg_nums,cnsvg_tags):
    header=str(no)
    header=header+'|<=>|'+str(kind)
    header=header+'|<=>|'+str(dfg)
    header=header+'|<=>|'+str(mfg)
    #print('del_flag=',str(dfg))
    header=header+'|<=>|'+str(svg_no)
    if(cnsvg_nums==None):
        cnsvg_nums=0
    header=header+'|<=>|'+str(cnsvg_nums)
    header=header+'|<=>|'+str(cnsvg_tags)
    return header
# ------------------------------------------------------------------    
def my_header2(no,kind,dfg):
    header=str(no)
    header=header+'|<=>|'+str(kind)
    header=header+'|<=>|'+str(dfg)
    return header
# ------------------------------------------------------------------    
def my_overviews(theme,bunrui1,bunrui2,bunrui3,day_regist,day_modify,author,overview,keywords):
    overviews=theme+'|<=>|'+bunrui1+'|<=>|'+bunrui2+'|<=>|'+bunrui3+'|<=>|'+day_regist+'|<=>|'+day_modify
    overviews=overviews+'|<=>|'+author+'|<=>|'+overview+'|<=>|'+keywords
    return overviews
# ------------------------------------------------------------------    
def update(request):
    global db_data,svg_data
    tex = request.POST.get("description",None)
    my_header= request.POST.get("my_header",None)
    header=my_header.split('|<=>|')
    #print('header=',header)
    data_id=int(header[0])
    svg_id=int(header[4])
    my_overview= request.POST.get("my_overview",None)
    overvw=my_overview.split('|<=>|')
    print('overviews=',overvw)
    cnnums= request.POST.get("cnsvg_nums",None)
    cnheader= request.POST.get("cnsvg_header",None)
    #print('cnsvg num=',cnnums,'header=',cnheader)
    svg_field = request.POST.get("svg",None)
    svg_field=svg_field.strip()
    try:
        db_data = My_Data.objects.get(pk=data_id)
        svg_data=My_Svg.objects.get(pk=svg_id)
        set_my_data(header,overvw)
        set_my_head(cnnums,cnheader)
        #print('***Update data=',db_data)
        #print('***SVG data=',svg_field)
        db_data.description = tex
        svg_data.svg_tags=svg_field
        db_data.save()
        svg_data.save()
        context='update!'
    except My_Data.DoesNotExist:
        raise Http404("da_data does not exist")
    return JsonResponse(data=[context,], safe=False)
# ------------------------------------------------------------------    
def update_GET(request):
    global db_data,svg_data
    tex = request.GET.get("description")
    my_header= request.GET.get("my_header")
    #print('my_header=',my_header,'tex=',tex)
    header=my_header.split('|<=>|')
    print('header=',header)
    data_id=int(header[0])
    svg_id=int(header[4])
    my_overview= request.GET.get("my_overview")
    overvw=my_overview.split('|<=>|')
    #print('overviews=',overvw)
    cnnums= request.GET.get("cnsvg_nums")
    cnheader= request.GET.get("cnsvg_header")
    #print('cnsvg num=',cnnums,'header=',cnheader)
    svg_field = request.GET.get("svg")
    svg_field=svg_field.strip()
    try:
        db_data = My_Data.objects.get(pk=data_id)
        svg_data=My_Svg.objects.get(pk=svg_id)
        set_my_data(header,overvw)
        set_my_head(cnnums,cnheader)
        #print('***Update data=',db_data)
        #print('***SVG data=',svg_field)
        db_data.description = tex
        svg_data.svg_tags=svg_field
        db_data.save()
        svg_data.save()
    except My_Data.DoesNotExist:
        raise Http404("da_data does not exist")
    return HttpResponse('update!')
# ------------------------------------------------------------------    
def update_sys(request):
    #print("**Start update_sys")
    #data_id=request.GET.get("rec_num")
    #script = request.GET.get("script")
    data_id=request.POST.get("rec_num")
    script = request.POST.get("script")

    try:
        db_data = My_Sys.objects.get(pk=data_id)
        db_data.description = script
        if(data_id=="1"):
            db_data.bunrui3="sysparms"
        if(data_id=="2"):
            db_data.bunrui3="html_tag"
        db_data.save()
        print("update_sys pk and no ="+str(db_data.id)+'   '+data_id+'   '+str(db_data.no))
    except My_Sys.DoesNotExist:
        raise Http404("da_data does not exist")
    return HttpResponse('script saved!')
# ------------------------------------------------------------------    
def get_timing(request):
    #print("**Start get_timing")
    data_id = request.GET.get("rec_num")
    #print("rec_num= "+ data_id)
    data = My_Sys.objects.get(pk=data_id)
    script=data.description
    
    #if(data_id=="1"):
        #if(data.bunrui3!="sysparms"):
            #script=""
    #if(data_id=="2"):
        #if(data.bunrui3!="html_tag"):
            #script=""
   
    context = {
        'script':script,
        }
    
    return JsonResponse(context)
# ------------------------------------------------------------------    
"""""
def update_head(request):
    global db_data,svg_data
    my_pk=request.GET.get("my_data_pk")
    nums= request.GET.get("cnsvg_nums")
    header= request.GET.get("cnsvg_header")
    print('pk=',my_pk,'cnsvg_nums=',nums,'cnsvg_header=',header)
    try:
        db_data = My_Data.objects.get(pk=my_pk)
        set_my_head(nums,header)
        print('***Update header=',header)
        db_data.save()
        header=my_header(db_data.no,0,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)

        context = {
        'header':header,
        }
    except My_Data.DoesNotExist:
        raise Http404("da_data does not exist")
    #return HttpResponse('update header!')
    return JsonResponse(context)
"""""
# ------------------------------------------------------------------    
def set_my_data(header,overvw):
    global db_data,svg_data
    db_data.no=int(header[0])
    db_data.kind= header[1]
    db_data.dfg=False
    if header[2]=='True':
        db_data.dfg = True
    db_data.mfg=False
    if header[3]=='True':
        db_data.mfg = True
    #print('dfg mfg=',db_data.dfg,db_data.mfg)
    db_data.svg_no = int(header[4])
    db_data.cnsvg_nums = int(header[5])
    db_data.cnsvg_tags = header[6]
    db_data.theme = overvw[0]
    db_data.bunrui1 = overvw[1]
    db_data.bunrui2 = overvw[2]
    db_data.bunrui3 = overvw[3]
    db_data.day_regist = overvw[4]
    db_data.day_modify = overvw[5]
    db_data.author = overvw[6]
    db_data.overview = overvw[7]
    db_data.keywords = overvw[8]
    svg_data.no=int(header[4])
    return
# ------------------------------------------------------------------    
def set_my_head(nums,header):
    global db_data,svg_data
    db_data.cnsvg_nums = nums
    db_data.cnsvg_tags = header
    return
# ------------------------------------------------------------------    
def newrec(request):
    global db_data,svg_data
    print('***Enter newrec')
    
    tex = request.GET.get("description")
    svg_field = request.GET.get("svg")
    svg_field=svg_field.strip()
    my_overview= request.GET.get("my_overview")
    #print(my_overview)
    overvw=my_overview.split('|<=>|')
    #print(overvw)
    
    my= My_Data.objects.create()
    my.no = my.pk
    my.cnsvg_nums=0
    my.cnsvg_tags=''
    my.theme = overvw[0]
    my.bunrui1 = overvw[1]
    my.bunrui2 = overvw[2]
    my.bunrui3 = overvw[3]
    my.day_regist = overvw[4]
    my.day_modify = overvw[5]
    my.author= overvw[6]
    my.overview = overvw[7]
    my.description = tex
    my.keywords= overvw[8]
    mysvg=My_Svg.objects.create()
    mysvg.no=mysvg.pk
    mysvg.svg_tags= svg_field
    mysvg.save()
    my.svg_no=mysvg.pk
    my.save()
    pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,0)
            
    all_save()
    
    header=my_header(my.no,0,my.dfg,my.mfg,my.svg_no,my.cnsvg_nums,my.cnsvg_tags)
    overviews=my_overviews(my.theme,my.bunrui1,my.bunrui2,my.bunrui3,my.day_regist,my.day_modify,my.author,my.overview,my.keywords)
    view_tex=tex
    """
    context = {
        'header':header,
        'overviews':overviews,
        'view_tex': view_tex,
        'svg_field': svg_field,
        }
    """
    context = {
        'rec_numb':my.no,
        }    
    #return HttpResponse('newrec!')
    return JsonResponse(context)
# ------------------------------------------------------------------    
def copynew(request):
    #print('***Enter copynew')
    tex = request.POST.get("description")
    headerh= request.POST.get("my_header")
    header=headerh.split('|<=>|')
    #print('header=',header)
    data_id=int(header[0])
    svg_id=int(header[4])
    cnsvg_nums=int(header[5])
    cnsvg_tags=header[6]
    my_overview= request.POST.get("my_overview")
    overvw=my_overview.split('|<=>|')
    #print('overviews=',overvw)
    svg_field = request.POST.get("svg")
    svg_field=svg_field.strip()
    
    dtime = datetime.now()
    nnowstr = dtime.strftime('%Y-%m-%d')
    
    my= My_Data.objects.create()
    my.no = my.pk
    my.theme = overvw[0]
    my.bunrui1 = overvw[1]
    my.bunrui2 = overvw[2]
    my.bunrui3 = overvw[3]
    my.day_regist = nnowstr
    my.day_modify = nnowstr
    my.author= overvw[6]
    my.overview = overvw[7]
    my.keywords= overvw[8]
    my.description = tex
    mysvg=My_Svg.objects.create()
    mysvg.no=mysvg.pk
    mysvg.svg_tags=svg_field
    mysvg.save()
    my.svg_no=mysvg.pk
    my.save()
    pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,0)
            
    all_save()
    
    header=my_header(my.no,0,my.dfg,my.mfg,my.svg_no,my.cnsvg_nums,my.cnsvg_tags)
    overviews=my_overviews(my.theme,my.bunrui1,my.bunrui2,my.bunrui3,my.day_regist,my.day_modify,my.author,my.overview,my.keywords)
    view_tex=tex
    
    if(cnsvg_nums>0):
        tags=cnsvg_tags.split(';')
        new_tags=''
        #print('tags=',tags)
        for k in range(cnsvg_nums):
            nums=tags[k].split(',')
            #print('cnsvg recnum=',nums[1])
            cn_old = My_CnSvg.objects.get(pk=nums[1])
            cnsvg=My_CnSvg.objects.create()
            cnsvg.no=cnsvg.pk
            cnsvg.kind='CnSvg'
            cnsvg.dfg=0
            cnsvg.mfg=0
            cnsvg.svg_tags=cn_old.svg_tags
            cnsvg.save()
            nums[1]=cnsvg.pk
            new_tags=new_tags+nums[0]+','+str(nums[1])+';'
        my.cnsvg_tags=new_tags
        my.save()
    
    """
    更にChain Svgに関して新たに各Chain SvgをCopyして新規レコードとして作成する
    context = {
        'header':header,
        'overviews':overviews,
        'view_tex': view_tex,
        'svg_field': svg_field,
        }
    """
    context = {
        'rec_numb':my.no,
        }    
    #return HttpResponse('newrec!')
    return JsonResponse(context)
# ------------------------------------------------------------------    
def copynew_bk(request):
    #print('***Enter copynew')
    tex = request.GET.get("description")
    headerh= request.GET.get("my_header")
    header=headerh.split('|<=>|')
    #print('header=',header)
    data_id=int(header[0])
    svg_id=int(header[4])
    cnsvg_nums=int(header[5])
    cnsvg_tags=header[6]
    my_overview= request.GET.get("my_overview")
    overvw=my_overview.split('|<=>|')
    #print('overviews=',overvw)
    svg_field = request.GET.get("svg")
    svg_field=svg_field.strip()
    
    dtime = datetime.now()
    nnowstr = dtime.strftime('%Y-%m-%d')
    
    my= My_Data.objects.create()
    my.no = my.pk
    my.theme = overvw[0]
    my.bunrui1 = overvw[1]
    my.bunrui2 = overvw[2]
    my.bunrui3 = overvw[3]
    my.day_regist = nnowstr
    my.day_modify = nnowstr
    my.author= overvw[6]
    my.overview = overvw[7]
    my.keywords= overvw[8]
    my.description = tex
    mysvg=My_Svg.objects.create()
    mysvg.no=mysvg.pk
    mysvg.svg_tags=svg_field
    mysvg.save()
    my.svg_no=mysvg.pk
    my.save()
    pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,0)
            
    all_save()
    
    header=my_header(my.no,0,my.dfg,my.mfg,my.svg_no,my.cnsvg_nums,my.cnsvg_tags)
    overviews=my_overviews(my.theme,my.bunrui1,my.bunrui2,my.bunrui3,my.day_regist,my.day_modify,my.author,my.overview,my.keywords)
    view_tex=tex
    
    if(cnsvg_nums>0):
        tags=cnsvg_tags.split(';')
        new_tags=''
        #print('tags=',tags)
        for k in range(cnsvg_nums):
            nums=tags[k].split(',')
            #print('cnsvg recnum=',nums[1])
            cn_old = My_CnSvg.objects.get(pk=nums[1])
            cnsvg=My_CnSvg.objects.create()
            cnsvg.no=cnsvg.pk
            cnsvg.kind='CnSvg'
            cnsvg.dfg=0
            cnsvg.mfg=0
            cnsvg.svg_tags=cn_old.svg_tags
            cnsvg.save()
            nums[1]=cnsvg.pk
            new_tags=new_tags+nums[0]+','+str(nums[1])+';'
        my.cnsvg_tags=new_tags
        my.save()
    
    """
    更にChain Svgに関して新たに各Chain SvgをCopyして新規レコードとして作成する
    context = {
        'header':header,
        'overviews':overviews,
        'view_tex': view_tex,
        'svg_field': svg_field,
        }
    """
    context = {
        'rec_numb':my.no,
        }    
    #return HttpResponse('newrec!')
    return JsonResponse(context)
# ------------------------------------------------------------------    
def save_cnsvg(request):
    #print('***Svave Chain_Svg')
    headerh= request.POST.get("cn_header")
    #print('headerh=',headerh)
    header=headerh.split(',')
    #print('header=',header)
    svg_field = request.POST.get("svg")
    svg_field=svg_field.strip()
    
    no = int(header[0])
    #kind=header[1]
    #dfg = header[2]
    #mfg = header[3]
    
    if(no==0):
        cnsvg=My_CnSvg.objects.create()
        cnsvg.no=cnsvg.pk
        cnsvg.kind='CnSvg'
        cnsvg.dfg=0
        cnsvg.mfg=0
    else:
        cnsvg=My_CnSvg.objects.get(pk=no)
        
    cnsvg.svg_tags=svg_field
    cnsvg.save()

    header=cn_header(cnsvg.no,cnsvg.kind,cnsvg.dfg,cnsvg.mfg)

    context = {
        'header':header,
        }
    
    #return HttpResponse('newrec!')
    return JsonResponse(context)
# ------------------------------------------------------------------    
def cn_header(no,kind,dfg,mfg):
    header=str(no)
    header=header+','+str(kind)
    header=header+','+str(dfg)
    header=header+','+str(mfg)
    return header
# ------------------------------------------------------------------    
def get_cnsvg(request):
    #print("**Start get_Reg_Svg** recieve ")
    data_id = request.GET.get("rec_number")
    #print("rec_number= "+ data_id)
    cnsvg = My_CnSvg.objects.get(pk=data_id)
    svg_field=''
    if(cnsvg.svg_tags!=''):
        svg_field = cnsvg.svg_tags
        svg_field=svg_field.strip()
        
    header=cn_header(cnsvg.no,cnsvg.kind,cnsvg.dfg,cnsvg.mfg)

    context = {
        'header':header,
        'svg_field':svg_field,
        }
    
    return JsonResponse(context)
# ------------------------------------------------------------------
def upload_add_formatcsv(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        sys.stderr.write("*** Enter POST file_upload *** aaa ***\n")
        if form.is_valid():
            sys.stderr.write("*** file_upload done *** aaa ***\n")
            rfile=handle_uploaded_file(request.FILES['file'])
            file_obj = request.FILES['file']
            sys.stderr.write(file_obj.name + "\n")
            
            print('file_path= ',rfile)
            f = open(rfile,'r',encoding='cp932')
            reader = csv.reader(f)
            ncnt=0
            pk_num=0
            
            for line in reader:
                ncnt=ncnt+1
                my = My_Data.objects.create()
                print('***DB',my.pk)
                print('data=',line[0],line[1],line[2],line[3])
                my.no = my.pk
                my.theme = line[1]
                my.bunrui1 = line[2]
                my.bunrui2 = line[3]
                my.bunrui3 = line[4]
                my.day_regist = line[5]
                my.day_modify = line[5]
                my.overview = decode(line[6])
                my.description = decode(line[7])
                my.keywords=''
                print('***count=',ncnt,'data=',my.theme,my.bunrui1,my.bunrui2,my.bunrui3)
                mysvg=My_Svg.objects.create()
                mysvg.no=mysvg.pk
                mysvg.svg_tags=''
                mysvg.save()
                my.svg_no=mysvg.pk
                my.save()
                pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,pk_num)
            
            all_save()

            return HttpResponse('complete!')
    else:
        form = UploadFileForm()
    return render(request, 'db_serv/upload.html', {'form': form})
#
# ------------------------------------------------------------------
def set_index(set,pkno,key0,key1,key2,key3,pk_num):
    global l0_keys
    global l0_nums
    global l0_nn
    global l1_keys
    global l1_nums
    global l1_nn
    global l2_keys
    global l2_nums
    global l2_nn
    global l3_keys
    global l3_nums
    global l3_nn
    #global recs_nums
    
    #global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0
    
    global pk_l0
    global pk_l1
    global pk_l2
    global pk_l3
    #global pk_recs
    
    """
    ixdata.kind='Ind'
    ixdata.mfg = False
    ixdata.level= 0
    ixdata.rec_num= 0
    ixdata.key_num= 0
    ixdata.key_tags = ''    
    """
    if(set==True):
        #ixdata_0=My_Index.objects.create()
        ixdata_0,pk_num=My_Index_create(1)
        pk_l0=ixdata_0.pk
        ixdata_0.no=ixdata_0.pk
        ixdata_0.kind='Ind'
        ixdata_0.level=0
        ixdata_0.mfg=True
        ixdata_0.rec_num=0
        ixdata_0.key_nums=1

        #ixdata_1=My_Index.objects.create()
        ixdata_1,pk_num=My_Index_create(2)
        pk_l1=ixdata_1.pk
        ixdata_1.no=ixdata_1.pk
        l0_nums[0]=ixdata_1.pk
        ixdata_1.kind='Ind'
        ixdata_1.level=1
        ixdata_1.mfg=True
        ixdata_1.rec_num=0
        ixdata_1.key_nums=1

        #ixdata_2=My_Index.objects.create()
        ixdata_2,pk_num=My_Index_create(3)
        pk_l2=ixdata_2.pk
        ixdata_2.no=ixdata_2.pk
        l1_nums[0]=ixdata_2.pk
        ixdata_2.kind='Ind'
        ixdata_2.level=2
        ixdata_2.mfg=True
        ixdata_2.rec_num=0
        ixdata_2.key_nums=1

        #ixdata_3=My_Index.objects.create()
        ixdata_3,pk_num=My_Index_create(4)
        pk_l3=ixdata_3.pk
        ixdata_3.no=ixdata_3.pk
        l2_nums[0]=ixdata_3.pk
        ixdata_3.kind='Ind'
        ixdata_3.level=3
        ixdata_3.mfg=True
        ixdata_3.rec_num=0
        ixdata_3.key_nums=1
        
        
        ixdata_3.key_tags=tags_compose([''],[0],[1])
        ixdata_2.key_tags=tags_compose([''],[pk_l3],[1])
        ixdata_1.key_tags=tags_compose([''],[pk_l2],[1])
        ixdata_0.key_tags=tags_compose([''],[pk_l1],[1])
        ixdata_3.save()
        ixdata_2.save()
        ixdata_1.save()
        ixdata_0.save()
        """
        recs_data=My_Recs.objects.create()
        pk_recs=recs_data.pk
        recs_data.no=recs_data.pk
        l3_nums[0]=recs_data.pk
        recs_data.kind='Recs'
        recs_data.rec_num=0
        recs_nums=[]
        pk_recs=recs_data.pk
        """
        print('Index initialized ix_0=',pk_l0,'ix_1=',pk_l1,'ix_2=',pk_l2,'ix_3=',pk_l3)
        return pk_num
    
    #level0のkey0のに対するkey登録と対応するlevel1indexの登録Logic
    if(pk_num==0):
        ixdata_0 = My_Index.objects.get(pk=1)
        pk_l0=1
        l0_keys,l0_nums,l0_nn=tags_decompose(ixdata_0.key_tags)
        ixdata_1 = My_Index.objects.get(pk=2)
        l1_keys,l1_nums,l1_nn=tags_decompose(ixdata_1.key_tags)
        ixdata_1.mfg=False
        ixdata_2 = My_Index.objects.get(pk=3)
        l2_keys,l2_nums,l2_nn=tags_decompose(ixdata_2.key_tags)
        ixdata_2.mfg=False
        ixdata_3 = My_Index.objects.get(pk=4)
        l3_keys,l3_nums,l3_nn=tags_decompose(ixdata_3.key_tags)
        ixdata_3.mfg=False
        pk_l1=2
        pk_l2=3
        pk_l3=4
        

    npk=match_key(l0_keys,key0)
    #print('L0 matchkey=',npk,key0,l0_keys,l0_nums,l0_nn)
    #既にkeyが登録されている場合(matchしない場合はnpk<0で返す)
    if(npk>=0):
        l0_nn[npk]+=1
        if(npk!=pk_l1):
            if(ixdata_1.mfg==True):
                ixdata_1.key_tags=tags_compose(l1_keys,l1_nums,l1_nn)
                ixdata_1.save()
            pk_l1=l0_nums[npk]
            #print('first pk_11=',pk_l1)
            ixdata_1 = My_Index.objects.get(pk=pk_l1)
            l1_keys,l1_nums,l1_nn=tags_decompose(ixdata_1.key_tags)

    else:
        #keyが登録されていない場合  使用中のixdata_1が追加されていたらsaveする
        if(ixdata_1.mfg==True):
            #ixdataのkey_tagsを編集してsaveする
            ixdata_1.key_tags=tags_compose(l1_keys,l1_nums,l1_nn)
            ixdata_1.save()
        #ixdata_1=My_Index.objects.create()
        ixdata_1,pk_num=My_Index_create(pk_num)
        ixdata_1.no=ixdata_1.pk
        ixdata_1.kind='Ind'
        ixdata_1.level=1
        ixdata_1.rec_num=0
        ixdata_1.key_nums=0
        l1_nums=[]
        l1_keys=[]
        l1_nn=[]
        pk_l1=ixdata_1.pk
        l0_nums.append(ixdata_1.pk)
        l0_keys.append(key0)
        l0_nn.append(int(1))
        ixdata_0.key_nums=ixdata_0.key_nums+1

    #level1のkey1のに対するkey登録と対応するlevel2indexの登録Logic
    npk=match_key(l1_keys,key1)
    #print('L1 matchkey=',npk,key1,l1_keys,l1_nums)
    #既にkeyが登録されている場合(matchしない場合はnpk<0で返す)
    if(npk>=0):
        l1_nn[npk]+=1
        if(npk!=pk_l2):
            if(ixdata_2.mfg==True):
                ixdata_2.key_tags=tags_compose(l2_keys,l2_nums,l2_nn)
                ixdata_2.save()
            pk_l2=l1_nums[npk]
            ixdata_2 = My_Index.objects.get(pk=pk_l2)
            l2_keys,l2_nums,l2_nn=tags_decompose(ixdata_2.key_tags)

    else:
        #keyが登録されていない場合  使用中のixdata_1が追加されていたらsaveする
        if(ixdata_2.mfg==True):
            #ixdataのkey_tagsを編集してsaveする
            ixdata_2.key_tags=tags_compose(l2_keys,l2_nums,l2_nn)
            ixdata_2.save()
        #ixdata_2=My_Index.objects.create()
        ixdata_2,pk_num=My_Index_create(pk_num)
        ixdata_2.no=ixdata_2.pk
        ixdata_2.kind='Ind'
        ixdata_2.level=2
        ixdata_2.rec_num=0
        ixdata_2.key_nums=0
        l2_nums=[]
        l2_keys=[]
        l2_nn=[]
        pk_l2=ixdata_2.pk
        
        l1_nums.append(ixdata_2.pk)
        l1_keys.append(key1)
        l1_nn.append(int(1))
        ixdata_1.key_nums=ixdata_1.key_nums+1
    
    #level2のkey2のに対するkey登録と対応するlevel2indexの登録Logic
    npk=match_key(l2_keys,key2)
    #print('L2 matchkey=',npk,key2,l2_keys,l2_nums)
    #既にkeyが登録されている場合(まtchしない場合はnpk<0で返す)
    if(npk>=0):
        l2_nn[npk]+=1
        if(npk!=pk_l3):
            if(ixdata_3.mfg==True):
                ixdata_3.key_tags=tags_compose(l3_keys,l3_nums,l3_nn)
                ixdata_3.save()
            pk_l3=l2_nums[npk]
            ixdata_3 = My_Index.objects.get(pk=pk_l3)
            l3_keys,l3_nums,l3_nn=tags_decompose(ixdata_3.key_tags)

    else:
        #keyが登録されていない場合  使用中のixdata_1が追加されていたらsaveする
        if(ixdata_3.mfg==True):
            #ixdataのkey_tagsを編集してsaveする
            ixdata_3.key_tags=tags_compose(l3_keys,l3_nums,l3_nn)
            ixdata_3.save()
        #ixdata_3=My_Index.objects.create()
        ixdata_3,pk_num=My_Index_create(pk_num)
        ixdata_3.no=ixdata_3.pk
        ixdata_3.kind='Ind'
        ixdata_3.level=3
        ixdata_3.mfg=True
        ixdata_3.rec_num=0
        ixdata_3.key_nums=0
        l3_nums=[]
        l3_keys=[]
        l3_nn=[]
        pk_l3=ixdata_3.pk
        
        l2_nums.append(ixdata_3.pk)
        l2_keys.append(key2)
        l2_nn.append(int(1))
        ixdata_2.key_nums=ixdata_2.key_nums+1
        
    #level3のkey3のに対するkey登録と対応するMy_Recsの登録Logic
    npk=match_key(l3_keys,key3)
    #print('L3 matchkey=',npk,key3,l3_keys,l3_nums)
    if(npk>=0):
        l3_nn[npk]+=1
        """
        if(npk!=pk_recs):
            if(recs_data.mfg==True):
                recs_data.tags=recs_compose(recs_nums)
                recs_data.save()
            pk_recs=l3_nums[npk]
            print('keys=',l3_keys,'nums=',l3_nums,'key3=',key3,'npk=',npk)
            recs_data = My_Recs.objects.get(pk=pk_recs)
            recs_nums=recs_decompose(recs_data.tags)
        """

    else:
        #keyが登録されていない場合  使用中のixdata_1が追加されていたらsaveする
        """
        if(recs_data.mfg==True):
            #ixdataのkey_tagsを編集してsaveする
            recs_data.tags=recs_compose(recs_nums)
            recs_data.save()
        recs_data=My_Recs.objects.create()
        recs_data.no=recs_data.pk
        recs_data.kind='Recs'
        recs_data.rec_num=0
        recs_nums=[]
        pk_recs=recs_data.pk
        
        l3_nums.append(recs_data.pk)
        """
        l3_nums.append(int(0))
        l3_keys.append(key3)
        l3_nn.append(int(1))
        ixdata_3.key_nums=ixdata_3.key_nums+1
        
    
    ixdata_0.rec_num=ixdata_0.rec_num+1
    ixdata_0.mfg=True
    ixdata_1.rec_num=ixdata_1.rec_num+1
    ixdata_1.mfg=True    
    ixdata_2.rec_num=ixdata_2.rec_num+1
    ixdata_2.mfg=True
    ixdata_3.rec_num=ixdata_3.rec_num+1
    ixdata_3.mfg=True    
    #recs_data.rec_num=recs_data.rec_num+1
    #recs_nums.append(pkno)
    #recs_data.mfg=True

    return pk_num
#
# ------------------------------------------------------------------
def My_Index_create(pk_num):
    if(pk_num==0):
        obj=My_Index.objects.create()
        #print('Create By system pk_num=',pk_num,obj.pk)
    else:
        obj,created=My_Index.objects.get_or_create(pk=pk_num)
        #print('Create=',created,'pk_num=',pk_num,obj.pk)
        pk_num=pk_num+1
    return obj,pk_num
# ------------------------------------------------------------------
def all_save():
    
    global l0_keys
    global l0_nums
    global l0_nn
    global l1_keys
    global l1_nums
    global l1_nn
    global l2_keys
    global l2_nums
    global l2_nn
    global l3_keys
    global l3_nums
    global l3_nn
    #global recs_nums    
    
    #global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0
    
    """
    if(recs_data.mfg==True):
        tags=recs_compose(recs_nums)
        recs_data.tags=tags
        recs_data.save()
    print('Recs_rec pk=',recs_data.pk)
    """
    if(ixdata_3.mfg==True):
        tags=tags_compose(l3_keys,l3_nums,l3_nn)
        ixdata_3.key_tags=tags
        ixdata_3.save()
    if(ixdata_2.mfg==True):
        tags=tags_compose(l2_keys,l2_nums,l2_nn)
        ixdata_2.key_tags=tags
        ixdata_2.save()
    if(ixdata_1.mfg==True):
        tags=tags_compose(l1_keys,l1_nums,l1_nn)
        ixdata_1.key_tags=tags
        ixdata_1.save()
    if(ixdata_0.mfg==True):
        tags=tags_compose(l0_keys,l0_nums,l0_nn)
        ixdata_0.key_tags=tags
        ixdata_0.save()

    #print('recs_data',recs_data.no,recs_data.tags)
    #print('ixdata_3',ixdata_3.no,ixdata_3.key_tags)
    #print('ixdata_2',ixdata_2.no,ixdata_2.key_tags)
    #print('ixdata_1',ixdata_1.no,ixdata_1.key_tags)
    #print('ixdata_0',ixdata_0.no,ixdata_0.key_tags)
    
    return
#
# -----------------------------------------------------------------
def upload_csv_todb(request):
    global g_upload_fg
    global g_pk_num
    global g_my_sys_num
    global g_my_data_num
    global g_my_svg_num
    global g_my_cnsvg_num
    global my_oldno
    global my_olddfg
    
    g_pk_num=0
    g_my_sys_num=0
    g_my_data_num=0
    g_my_svg_num=0
    g_my_cnsvg_num=0
    g_upload_fg=1
    my_oldno=0
    print('initial set')   
    
    return render(request, 'db_serv/upload_csv_todb.html',{})
# -----------------------------------------------------------------
def setup_csv_record(request):
    
    global l0_keys
    global l0_nums
    global l0_nn
    global l1_keys
    global l1_nums
    global l1_nn
    global l2_keys
    global l2_nums
    global l2_nn
    global l3_keys
    global l3_nums
    global l3_nn
    #global recs_nums    
    
    #global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0

    global g_upload_fg
    global g_pk_num
    global g_my_sys_num
    global g_my_data_num
    global g_my_svg_num
    global g_my_cnsvg_num
    global my_oldno
    global my_olddfg    
    
    print('upload_init POST/GET=',request.method)
    if request.method == 'POST':
        kind=request.POST.get('kind', None)
        term1 = request.POST.get('term1', None)
        data_0 = request.POST.get('term2', None)
        data_1 = request.POST.get('term3', None)
        data_2 = request.POST.get('term4', None)

        print('old data kind=',kind,'header=',term1)
        recnum=save_rec_todb(kind,term1,data_0,data_1,data_2)

        if(kind=="finish"):
            #all_save()
            print('DB records my_data=',g_my_data_num,' my_svg=',g_my_svg_num,' my_cnsvg_num=',g_my_cnsvg_num)

        print('nums=',g_my_sys_num,g_my_data_num,g_my_svg_num,g_my_cnsvg_num)
    
        context = {
            'kind':kind,
            'rec_num':recnum,
            }
    return JsonResponse(context)
# ------------------------------------------------------------------
def save_rec_todb(kind,term1,data_0,data_1,data_2):
    global g_upload_fg
    global g_pk_num
    global g_my_sys_num
    global g_my_data_num
    global g_my_svg_num
    global g_my_cnsvg_num
    global my_oldno
    global my_olddfg
    global myold_cnsvgtags
    global old_cnsvg_nums
    
    mynum=0
    if(kind=="My_Sys"):
        my_sys,res=My_Sys.objects.get_or_create(pk=g_my_sys_num+1)
        my_sys.no=my_sys.pk
        my_sys.kind="My_Sys"
        my_sys.theme="system"
        my_sys.bunrui1=""
        my_sys.bunrui2=""
        my_sys.bunrui3=""
        my_sys.overview=""
        my_sys.description=data_0
        my_sys.save()
        g_my_sys_num+=1
        print('new My_Sys=',my_sys.kind,' no=',my_sys.no)
        mynum=my_sys.no
    
    if(kind=="My_Data"):
        header=term1.split('|<=>|')
        my_oldno=header[0]
        old_cnsvg_nums=header[5]
        myold_cnsvgtags=header[6].split(';')
        print('header=',header)
        print('old cnsvg_num=',header[5],' tags=',header[6])
        my,res=My_Data.objects.get_or_create(pk=g_my_data_num+1)
        my.no = my.pk
        my_oldno=my.no
        g_my_data_num+=1
        my.kind='My_Data'
        my.dfg=False
        my.mfg=False
        my_olddfg=False
        my.svg_no=header[4]
        my.cnsvg_nums=0
        my.cnsvg_tags=''
        overviews=data_0.split('|<=>|')
        print('overview=',overviews)
        my.theme=overviews[0]
        my.bunrui1=overviews[1]
        my.bunrui2=overviews[2]
        my.bunrui3=overviews[3]
        my.day_regist=overviews[4]
        my.day_modify=overviews[5]
        my.author=overviews[6]
        my.overview=overviews[7]
        my.keywords=overviews[8]
        my.description=data_1
        print('doc description=',data_1)
        my.save()
        print('new My_Data=',my.kind,' no=',my.no)
        mynum=my.no

    if((kind=="My_Svg") and (my_olddfg==False)):
        my_svg,res=My_Svg.objects.get_or_create(pk=g_my_svg_num+1)
        my_svg.no = my_svg.pk
        g_my_svg_num+=1
        my_svg.kind='My_Svg'
        my_svg.dfg=False
        my_svg.mfg=False
        my_svg.svg_tags=term1
        print('My_Svg data=',term1)
        my_svg.save()
        print('new My_Svg=',my_svg.kind,' no=',my_svg.no)
        my = My_Data.objects.get(pk=my_oldno)
        print('new My_Svg=',my_svg.kind,' no=',my_svg.no,'to My_Data=',my.no)
        my.svg_no=my_svg.no
        my.save()
        mynum=my_svg.no
            
    if((kind=="My_CnSvg") and (my_olddfg==False)):
        my_cnsvg,res=My_CnSvg.objects.get_or_create(pk=g_my_cnsvg_num+1)
        my_cnsvg.no = my_cnsvg.pk
        g_my_cnsvg_num+=1
        my_cnsvg.kind='My_CnSvg'
        my_cnsvg.dfg=False
        my_cnsvg.mfg=False
        my_cnsvg.svg_tags=term1
        print('My_CnSvg data=',term1)
        my_cnsvg.save()
        print('new My_CnSvg=',my_cnsvg.kind,' no=',my_cnsvg.no)
        mynum=my_cnsvg.no
        
        my = My_Data.objects.get(pk=my_oldno)
        my.cnsvg_nums+=1
        #tags=myold_cnsvgtags[my.cnsvg_nums-1].split(',')
        nwtags='svg_0'+str(my.cnsvg_nums)+","+str(my_cnsvg.no)+";"
        #print('new tag=',nwtags)
        my.cnsvg_tags=my.cnsvg_tags+nwtags
        #if(my.cnsvg_nums==int(old_cnsvg_nums)):
        my.save()
        print('new cnsvg_num=',my.cnsvg_nums,' tags=',my.cnsvg_tags,'to My_Data',my.no)
    
    return mynum
# ------------------------------------------------------------------
#最新バージョンのデータアップロード　http://127.0.0.1:8000/upload_init/
def upload_create(request):
    print('upload_init POST/GET=',request.method)
    csv.field_size_limit(1000000000)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        sys.stderr.write("*** Enter POST file_upload *** aaa ***\n")
        if form.is_valid():
            sys.stderr.write("*** file_upload done *** aaa ***\n")
            rfile=handle_uploaded_file(request.FILES['file'])
            file_obj = request.FILES['file']
            sys.stderr.write(file_obj.name + "\n")
            
            print('file_path= ',rfile)
            f = open(rfile,'r',encoding='utf8')
            reader = csv.reader(f)
            
        """
        My_Index.objects.all().delete()
        My_Data.objects.all().delete()
        My_Svg.objects.all().delete()
        My_CnSvg.objects.all().delete()
        My_Recs.objects.all().delete()
        
        #myind=My_Index.objects.all().only("no")
        #mydat=My_Data.objects.all().only("no")
        #mysvg=My_Svg.objects.all().only("no")
        #mycnsvg=My_CnSvg.objects.all().only("no")
        #print('Db rec numb ind=',len(myind),'dat=',len(mydat),'svg=',len(mysvg),'cnsvg=',len(mycnsvg))        
        """
        
        pk_num=0
        pk_num=set_index(True,0,'','','','',pk_num)

        my_sys_num=0
        my_data_num=0
        my_svg_num=0
        my_cnsvg_num=0
            
        for line in reader:
            my_no=line[0]
            no=line[1]
            kind=line[2]
            dfg=line[3]
            print('old data kind=',kind,' dfg=',dfg,' my_no=',my_no,' no=',no)
            #header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            data_0=line[4]
            #overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            data_1=line[5]
            #view_tex=db_data.description
            data_2=line[6]
            
            if(kind=='My_Sys'):
                my_sys,res=My_Sys.objects.get_or_create(pk=my_sys_num+1)
                
                my_sys.no=my_sys.pk
                my_sys.kind="My_Sys"
                my_sys.theme="system"
                my_sys.bunrui1=""
                my_sys.bunrui2=""
                my_sys.bunrui3=""
                my_sys.overview=""
                my_sys.description=data_0
                my_sys.save()
                my_sys_num+=1
                print('sys data kind=',my_sys.kind,' no=',my_sys.no,'data_0=',my_sys.description)
                
            if(kind=='My_Data'):
                header=data_0.split('|<=>|')
                my_oldno=header[0]
                old_cnsvg_nums=header[5]
                myold_cnsvgtags=header[6].split(';')
                my_dfg=dfg
                print('Enter My_Data dfg=',my_dfg)

                if(my_dfg=='False'):
                    #print('header=',header)
                    print('old cnsvg_num=',header[5],' tags=',header[6])
                    my,res=My_Data.objects.get_or_create(pk=my_data_num+1)
                    my.no = my.pk
                    my_data_num+=1
                    my.kind='My_Data'
                    my.dfg=False
                    my.mfg=False
                    my.svg_no=header[4]
                    my.cnsvg_nums=0
                    my.cnsvg_tags=''
                    overviews=data_1.split('|<=>|')
                    my.theme=overviews[0]
                    my.bunrui1=overviews[1]
                    my.bunrui2=overviews[2]
                    my.bunrui3=overviews[3]
                    my.day_regist=overviews[4]
                    my.day_modify=overviews[5]
                    my.author=overviews[6]
                    my.overview=overviews[7]
                    my.keywords=overviews[8]
                    my.description=data_2
                    my.save()
                    print('new data kind=',my.kind,' no=',my.no)
                    pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,pk_num)
            
            if((kind=='My_Svg') and (my_no==my_oldno) and (my_dfg=='False')):
                my_svg,res=My_Svg.objects.get_or_create(pk=my_svg_num+1)
                my_svg.no = my_svg.pk
                my_svg_num+=1
                my_svg.kind='My_Svg'
                my_svg.dfg=False
                my_svg.mfg=False
                my_svg.svg_tags=data_0
                my_svg.save()
                print('new data kind=',my_svg.kind,' no=',my_svg.no)
                my.svg_no=my_svg.no
                my.save()
                
            if((kind=='My_CnSvg') and (my_no==my_oldno) and (my_dfg=='False')):
                my_cnsvg,res=My_CnSvg.objects.get_or_create(pk=my_cnsvg_num+1)
                my_cnsvg.no = my_cnsvg.pk
                my_cnsvg_num+=1
                my_cnsvg.kind='My_CnSvg'
                my_cnsvg.dfg=False
                my_cnsvg.mfg=False
                my_cnsvg.svg_tags=data_0
                my_cnsvg.save()
                print('new data kind=',my_cnsvg.kind,' no=',my_cnsvg.no)
                    
                my.cnsvg_nums+=1
                tags=myold_cnsvgtags[my.cnsvg_nums-1].split(',')
                nwtags=tags[0]+","+str(my_cnsvg.no)+";"
                #print('new tag=',nwtags)
                my.cnsvg_tags=my.cnsvg_tags+nwtags
                if(my.cnsvg_nums==int(old_cnsvg_nums)):
                    my.save()
                    print('cnsvg_num=',my.cnsvg_nums,' tags=',my.cnsvg_tags)

            
        all_save()
        print('DB records my_data=',my_data_num,' my_svg=',my_svg_num,' my_cnsvg_num=',my_cnsvg_num)

        return HttpResponse('complete!')
    else:
        form = UploadFileForm()
    return render(request, 'db_serv/upload.html', {'form': form})
#
# ------------------------------------------------------------------
#最新バージョンのデータアップロード　http://127.0.0.1:8000/upload_init/
def upload_init(request):
    print('upload_init POST/GET=',request.method)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        sys.stderr.write("*** Enter POST file_upload *** aaa ***\n")
        if form.is_valid():
            sys.stderr.write("*** file_upload done *** aaa ***\n")
            rfile=handle_uploaded_file(request.FILES['file'])
            file_obj = request.FILES['file']
            sys.stderr.write(file_obj.name + "\n")
            
            print('file_path= ',rfile)
            f = open(rfile,'r',encoding='utf8')
            reader = csv.reader(f)

        My_Index.objects.all().delete()
        My_Data.objects.all().delete()
        My_Svg.objects.all().delete()
        My_CnSvg.objects.all().delete()
        My_Recs.objects.all().delete()
        
        #myind=My_Index.objects.all().only("no")
        #mydat=My_Data.objects.all().only("no")
        #mysvg=My_Svg.objects.all().only("no")
        #mycnsvg=My_CnSvg.objects.all().only("no")
        #print('Db rec numb ind=',len(myind),'dat=',len(mydat),'svg=',len(mysvg),'cnsvg=',len(mycnsvg))        
        
        pk_num=0
        pk_num=set_index(True,0,'','','','',pk_num)

        my_data_num=0
        my_svg_num=0
        my_cnsvg_num=0
            
        for line in reader:
            my_no=line[0]
            no=line[1]
            kind=line[2]
            dfg=line[3]
            print('old data kind=',kind,' dfg=',dfg,' my_no=',my_no,' no=',no)
            #header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            data_0=line[4]
            #overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            data_1=line[5]
            #view_tex=db_data.description
            data_2=line[6]
                
            if(kind=='My_Data'):
                header=data_0.split('|<=>|')
                my_oldno=header[0]
                old_cnsvg_nums=header[5]
                myold_cnsvgtags=header[6].split(';')
                my_dfg=dfg
                print('Enter My_Data dfg=',my_dfg)

                if(my_dfg=='False'):
                    #print('header=',header)
                    print('old cnsvg_num=',header[5],' tags=',header[6])
                    my,res=My_Data.objects.get_or_create(pk=my_data_num+1)
                    my.no = my.pk
                    my_data_num+=1
                    my.kind='My_Data'
                    my.dfg=False
                    my.mfg=False
                    my.svg_no=header[4]
                    my.cnsvg_nums=0
                    my.cnsvg_tags=''
                    overviews=data_1.split('|<=>|')
                    my.theme=overviews[0]
                    my.bunrui1=overviews[1]
                    my.bunrui2=overviews[2]
                    my.bunrui3=overviews[3]
                    my.day_regist=overviews[4]
                    my.day_modify=overviews[5]
                    my.author=overviews[6]
                    my.overview=overviews[7]
                    my.keywords=overviews[8]
                    my.description=data_2
                    my.save()
                    print('new data kind=',my.kind,' no=',my.no)
                    pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,pk_num)
            
            if((kind=='My_Svg') and (my_no==my_oldno) and (my_dfg=='False')):
                my_svg,res=My_Svg.objects.get_or_create(pk=my_svg_num+1)
                my_svg.no = my_svg.pk
                my_svg_num+=1
                my_svg.kind='My_Svg'
                my_svg.dfg=False
                my_svg.mfg=False
                my_svg.svg_tags=data_0
                my_svg.save()
                print('new data kind=',my_svg.kind,' no=',my_svg.no)
                my.svg_no=my_svg.no
                my.save()
                
            if((kind=='My_CnSvg') and (my_no==my_oldno) and (my_dfg=='False')):
                my_cnsvg,res=My_CnSvg.objects.get_or_create(pk=my_cnsvg_num+1)
                my_cnsvg.no = my_cnsvg.pk
                my_cnsvg_num+=1
                my_cnsvg.kind='My_CnSvg'
                my_cnsvg.dfg=False
                my_cnsvg.mfg=False
                my_cnsvg.svg_tags=data_0
                my_cnsvg.save()
                print('new data kind=',my_cnsvg.kind,' no=',my_cnsvg.no)
                    
                my.cnsvg_nums+=1
                tags=myold_cnsvgtags[my.cnsvg_nums-1].split(',')
                nwtags=tags[0]+","+str(my_cnsvg.no)+";"
                #print('new tag=',nwtags)
                my.cnsvg_tags=my.cnsvg_tags+nwtags
                if(my.cnsvg_nums==int(old_cnsvg_nums)):
                    my.save()
                    print('cnsvg_num=',my.cnsvg_nums,' tags=',my.cnsvg_tags)

            
        all_save()
        print('DB records my_data=',my_data_num,' my_svg=',my_svg_num,' my_cnsvg_num=',my_cnsvg_num)

        return HttpResponse('complete!')
    else:
        form = UploadFileForm()
    return render(request, 'db_serv/upload.html', {'form': form})
#
# ------------------------------------------------------------------
#最新バージョンのデータアップロードadd　http://127.0.0.1:8000/upload_add/
def upload_add(request):
    print('upload_init POST/GET=',request.method)
    csv.field_size_limit(1000000000)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        sys.stderr.write("*** Enter POST file_upload *** aaa ***\n")
        if form.is_valid():
            sys.stderr.write("*** file_upload done *** aaa ***\n")
            rfile=handle_uploaded_file(request.FILES['file'])
            file_obj = request.FILES['file']
            sys.stderr.write(file_obj.name + "\n")
            
            print('file_path= ',rfile)
            f = open(rfile,'r',encoding='utf8')
            reader = csv.reader(f)

        myind=My_Index.objects.all().only("no")
        mydat=My_Data.objects.all().only("no")
        mysvg=My_Svg.objects.all().only("no")
        mycnsvg=My_CnSvg.objects.all().only("no")
        print('Db rec numb ind=',len(myind),'dat=',len(mydat),'svg=',len(mysvg),'cnsvg=',len(mycnsvg))        
        
        my_data_num=len(mydat)
        my_svg_num=len(mysvg)
        my_cnsvg_num=len(mycnsvg)
        pk_num=0
        
        for line in reader:
            my_no=line[0]
            no=line[1]
            kind=line[2]
            dfg=line[3]
            print('old data kind=',kind,' dfg=',dfg,' my_no=',my_no,' no=',no)
            #header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            data_0=line[4]
            #overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            data_1=line[5]
            #view_tex=db_data.description
            data_2=line[6]
                
            if(kind=='My_Data'):
                header=data_0.split('|<=>|')
                my_oldno=header[0]
                old_cnsvg_nums=header[5]
                myold_cnsvgtags=header[6].split(';')
                my_dfg=dfg
                print('Enter My_Data dfg=',my_dfg)

                if(my_dfg=='False'):
                    #print('header=',header)
                    print('old cnsvg_num=',header[5],' tags=',header[6])
                    my,res=My_Data.objects.get_or_create(pk=my_data_num+1)
                    my.no = my.pk
                    my_data_num+=1
                    my.kind='My_Data'
                    my.dfg=False
                    my.mfg=False
                    my.svg_no=header[4]
                    my.cnsvg_nums=0
                    my.cnsvg_tags=''
                    overviews=data_1.split('|<=>|')
                    my.theme=overviews[0]
                    my.bunrui1=overviews[1]
                    my.bunrui2=overviews[2]
                    my.bunrui3=overviews[3]
                    my.day_regist=overviews[4]
                    my.day_modify=overviews[5]
                    my.author=overviews[6]
                    my.overview=overviews[7]
                    my.keywords=overviews[8]
                    my.description=data_2
                    my.save()
                    print('new data kind=',my.kind,' no=',my.no)
                    pk_num=set_index(False,my.no,my.theme,my.bunrui1,my.bunrui2,my.bunrui3,pk_num)
            
            if((kind=='My_Svg') and (my_no==my_oldno) and (my_dfg=='False')):
                my_svg,res=My_Svg.objects.get_or_create(pk=my_svg_num+1)
                my_svg.no = my_svg.pk
                my_svg_num+=1
                my_svg.kind='My_Svg'
                my_svg.dfg=False
                my_svg.mfg=False
                my_svg.svg_tags=data_0
                my_svg.save()
                print('new data kind=',my_svg.kind,' no=',my_svg.no)
                my.svg_no=my_svg.no
                my.save()
                
            if((kind=='My_CnSvg') and (my_no==my_oldno) and (my_dfg=='False')):
                my_cnsvg,res=My_CnSvg.objects.get_or_create(pk=my_cnsvg_num+1)
                my_cnsvg.no = my_cnsvg.pk
                my_cnsvg_num+=1
                my_cnsvg.kind='My_CnSvg'
                my_cnsvg.dfg=False
                my_cnsvg.mfg=False
                my_cnsvg.svg_tags=data_0
                my_cnsvg.save()
                print('new data kind=',my_cnsvg.kind,' no=',my_cnsvg.no)
                    
                my.cnsvg_nums+=1
                tags=myold_cnsvgtags[my.cnsvg_nums-1].split(',')
                nwtags=tags[0]+","+str(my_cnsvg.no)+";"
                #print('new tag=',nwtags)
                my.cnsvg_tags=my.cnsvg_tags+nwtags
                if(my.cnsvg_nums==int(old_cnsvg_nums)):
                    my.save()
                    print('cnsvg_num=',my.cnsvg_nums,' tags=',my.cnsvg_tags)

            
        all_save()
        print('DB records my_data=',my_data_num,' my_svg=',my_svg_num,' my_cnsvg_num=',my_cnsvg_num)

        return HttpResponse('complete!')
    else:
        form = UploadFileForm()
    return render(request, 'db_serv/upload.html', {'form': form})
#
# ------------------------------------------------------------------
def collect_rec(request):
    from datetime import date
    import csv
    
    global db_data,svg_data
    print("** collect_records ** recieve ")
    rec_str = request.GET.get("rec_str")
    data_id=rec_str.split(';')
    print("rec_numbers= ", rec_str)
    
    t = date.today()
    output_path = './'
    output_name = t.strftime('%Y%m%d') + '_collectrecs.csv'
    
    # CSV出力処理開始
    #f = open(wfile,'w',encoding='cp932',newline="")
    with open(output_path + output_name, 'w', encoding='utf8', newline='') as csv_file:
        # 1行目にヘッダーを書き込む
        header = ['My_no', 'no', 'kind', 'del', 'data_0', 'data_1', 'data_2']
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        
        # 検索対象レコードの抽出
        list = data_id[:-1]
        
        my_data_rec=0
        svg_data_rec=0
        cnsvg_data_rec=0
        for dat in list:
            db_data = My_Data.objects.get(pk=dat)
            my_no=db_data.no
            no=db_data.no
            kind='My_Data'
            dfg=db_data.dfg
            #header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            data_0=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            #overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            data_1=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            #view_tex=db_data.description
            data_2=db_data.description

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            my_data_rec+=1
            writer.writerow(row)
            
            split_h=data_0.split('|<=>|')
            svg_no=split_h[4]
            cnsdat=split_h[6].split(';')
            
            #Top svgデータの読み込みとcsvへのwrite
            svg_data=My_Svg.objects.get(pk=svg_no)
            my_no=db_data.no
            no=svg_data.no
            kind='My_Svg'
            dfg=svg_data.dfg
            data_0=svg_data.svg_tags
            data_1=''
            data_2=''

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            svg_data_rec+=1
            writer.writerow(row)
            
            print('svg_no=',svg_no,'cns dta=',split_h[6],cnsdat,'data len text and svg=',len(db_data.description),len(svg_data.svg_tags))
            
            for cns in cnsdat:
                rec=cns.split(',')
                reclen=len(rec)
                reject=''
                if(cns!='' and reclen!=2):
                    reject='cnsvg reject'
                    print('cnsvg data len=',reclen,rec,reject)
                
                if(cns!='' and reclen==2):
                    cnsvg_data=My_CnSvg.objects.get(pk=rec[1])
                    my_no=db_data.no
                    no=cnsvg_data.no
                    kind='My_CnSvg'
                    dfg=cnsvg_data.dfg
                    data_0=cnsvg_data.svg_tags
                    data_1=''
                    data_2=''                        
                    row = []
                    row += [my_no, no, kind, dfg, data_0, data_1, data_2]
                    cnsvg_data_rec+=1
                    writer.writerow(row)
        print('my_data nn=',my_data_rec,'svg_data nn=',svg_data_rec,'cnsvg_data nn=',cnsvg_data_rec)

    return HttpResponse('complete!')
# ------------------------------------------------------------------
def download_from_tocsv(request):
    return render(request, 'db_serv/download_from_tocsv.html',{})
# ------------------------------------------------------------------
def download_recs(request):
    global st_step;
    global n_sys_tot;
    global n_sys;
    global n_docs;
    global n_docs_tot;
    global ex_cnsvg
    global n_cnsvg_tot
    global nn_cnsvg
    global after_next
    global nn_list
    
    next=''
    header=''
    overviews=''
    view_tex=''
    svg_field=''
    
    print('download_recs POST/GET=',request.method)
    if request.method == 'POST':
        step_st = request.POST.get('step', None)
        print("download step= ", step_st)
        
        if(step_st=='start'):
            # 検索対象レコードの抽出
            nn_list = My_Sys.objects.only("no","kind","dfg").all().order_by("no")
            n_sys_tot=len(nn_list)
            #print('My_sys numb=',n_sys_tot,nn_list)
            n_sys=0
            header,overviews,view_tex,svg_field=get_mysys_rec(nn_list[n_sys].no)
            next='sys_next'
        if(step_st=='sys_next'):
            n_sys=n_sys+1
            print('My_Sys n_sys=',n_sys_tot,n_sys,nn_list[n_sys].no,nn_list[n_sys].kind)
            header,overviews,view_tex,svg_field=get_mysys_rec(nn_list[n_sys].no)
            if(n_sys<n_sys_tot-1):
                next='sys_next'
            else:
                header,overviews,view_tex,svg_field=get_mysys_rec(nn_list[n_sys].no)
                next='doc_start'

        if(step_st=='doc_start'):
            # 検索対象レコードの抽出
            nn_list = My_Data.objects.only("no","kind","dfg").all().order_by("no")
            n_docs_tot=len(nn_list)
            n_docs=0
            header,overviews,view_tex,svg_field=get_mydata_rec(nn_list[n_docs].no)
            print('My_Data n_docs=',n_docs_tot,n_docs,nn_list[n_docs].no,nn_list[n_docs].kind,'CnSvg num=',n_cnsvg_tot)
            if(n_cnsvg_tot>0):
                nn_cnsvg=0
                next='svg_start'
                if(n_docs<n_docs_tot-1):
                    after_next='doc_next'
                else:
                    after_next='finish'
                print('next=',next,'after at svg_start=',after_next)
            else:
                if(n_docs<n_docs_tot-1):
                    next='doc_next'
                else:
                    next='finish'
                
        if(step_st=='doc_next'):
            n_docs=n_docs+1
            header,overviews,view_tex,svg_field=get_mydata_rec(nn_list[n_docs].no)
            print('My_Data n_docs=',n_docs_tot,n_docs,nn_list[n_docs].no,nn_list[n_docs].kind,'CnSvg num=',n_cnsvg_tot)
            if(n_cnsvg_tot>0):
                next='svg_start'
                if(n_docs<n_docs_tot-1):
                    after_next='doc_next'
                else:
                    after_next='finish'
                print('next=',next,'after at svg_start=',after_next)
            else:
                if(n_docs<n_docs_tot-1):
                    next='doc_next'
                else:
                    next='finish'
                    
        if(step_st=='svg_start'):
            # 検索対象レコードの抽出
            print('before svg start=',after_next)
            nn_cnsvg=0
            cn_rec=ex_cnsvg[nn_cnsvg].split(',')
            print('My_CnSvg cnsvg_data=',ex_cnsvg,'cnsvg_num=',nn_cnsvg,'cnrec=',cn_rec[1],ex_cnsvg[nn_cnsvg],'after=',after_next)
            header,overviews,view_tex,svg_field=get_mycnsvg_rec(cn_rec[1])
            if(nn_cnsvg<n_cnsvg_tot-1):
                next='svg_next'
            else:
                next=after_next
        if(step_st=='svg_next'):
            # 検索対象レコードの抽出
            nn_cnsvg=nn_cnsvg+1
            cn_rec=ex_cnsvg[nn_cnsvg].split(',')
            print('My_CnSvg cnsvg_data=',ex_cnsvg,'cnsvg_num=',nn_cnsvg,'cnrec=',cn_rec[1],ex_cnsvg[nn_cnsvg],'after=',after_next)
            header,overviews,view_tex,svg_field=get_mycnsvg_rec(cn_rec[1])
            if(nn_cnsvg<n_cnsvg_tot-1):
                next='svg_next'
            else:
                next=after_next
            
        context = {
            'next':next,
            'header':header,
            'overviews':overviews,
            'view_tex': view_tex,
            'svg_field': svg_field,
            }
        
    return JsonResponse(context)
# ------------------------------------------------------------------
def get_mysys_rec(idno):
    
    db_data = My_Sys.objects.get(pk=idno)

    header=my_header2(db_data.no,db_data.kind,db_data.dfg)
    data_0=db_data.description
    #print('My_Sys data=',data_0)
    data_1=''
    data_2=''
    
    return header,data_0,data_1,data_2
# ------------------------------------------------------------------
def get_mycnsvg_rec(idno):
    
    db_data = My_CnSvg.objects.get(pk=idno)
    header=my_header2(db_data.no,db_data.kind,db_data.dfg)
    data_0=db_data.svg_tags

    data_1=''
    data_2=''
    
    return header,data_0,data_1,data_2
# ------------------------------------------------------------------
def get_mydata_rec(idno):
    global ex_cnsvg
    global n_cnsvg_tot
    global nn_cnsvg    

    db_data = My_Data.objects.get(pk=idno)
    view_tex=db_data.description
    #print('***Db_data id= ',db_data.no,' svg_no= ',db_data.svg_no,' overview=',db_data.overview,'cnsvg_tags= ',db_data.cnsvg_tags)
    ex_cnsvg=db_data.cnsvg_tags
    db_data.cnsvg_tags=''
    header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
    overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
    svg_data=My_Svg.objects.get(pk=db_data.svg_no)
    svg_field=''
    if(svg_data.svg_tags!=''):
        svg_field = svg_data.svg_tags
        svg_field=svg_field.strip()
        #print('**Svg=',svg_field)

    ex_cnsvg=ex_cnsvg.split(';')
    n_cnsvg_tot=db_data.cnsvg_nums
    
    return header,overviews,view_tex,svg_field
# ------------------------------------------------------------------
def sql_download(request):
    from datetime import date
    import csv

    t = date.today()
    output_path = './'
    output_name = t.strftime('%Y%m%d') + '_mysqldata.csv'
    
    # CSV出力処理開始
    #f = open(wfile,'w',encoding='cp932',newline="")
    with open(output_path + output_name, 'w', encoding='utf-8', newline='') as csv_file:
    #codecs.open(file_path, 'r', 'utf-8', 'ignore') as file:
    #with codecs.open(output_path + output_name, 'w', 'cp932','ignore') as csv_file:
        # 1行目にヘッダーを書き込む
        header = ['My_no', 'no', 'kind', 'del', 'data_0', 'data_1', 'data_2']
        #writer = csv.writer(csv_file, delimiter='\t', quoting=csv.QUOTE_ALL)
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        
        # 検索対象レコードの抽出
        list = My_Sys.objects.only("no","kind","dfg").all().order_by("no")
        #list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

        sys_data_rec=0
        for dat in list:
            db_data = My_Sys.objects.get(pk=dat.id)
        #for kk in list:
            #db_data = My_Sys.objects.get(pk=kk)       
            my_no=db_data.no
            no=db_data.no
            kind='My_Sys'
            dfg=db_data.dfg
            data_0=db_data.description
            data_1=''
            data_2=''
            
            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            sys_data_rec+=1
            writer.writerow(row)
            
            print('My_Sys num=',sys_data_rec,my_no,'kind=',kind,'del flg=',dfg)
                    
        # 検索対象レコードの抽出
        list = My_Data.objects.only("no","kind","dfg").all().order_by("no")
        
        my_data_rec=0
        svg_data_rec=0
        cnsvg_data_rec=0
        for dat in list:
            db_data = My_Data.objects.get(pk=dat.no)
            my_no=db_data.no
            no=db_data.no
            kind='My_Data'
            dfg=db_data.dfg
            #header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            data_0=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            #overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            data_1=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            #view_tex=db_data.description
            data_2=db_data.description

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            my_data_rec+=1
            writer.writerow(row)
            
            split_h=data_0.split('|<=>|')
            svg_no=split_h[4]
            cnsdat=split_h[6].split(';')
            
            #Top svgデータの読み込みとcsvへのwrite
            svg_data=My_Svg.objects.get(pk=svg_no)
            my_no=db_data.no
            no=svg_data.no
            kind='My_Svg'
            dfg=svg_data.dfg
            data_0=svg_data.svg_tags
            data_1=''
            data_2=''

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            svg_data_rec+=1
            writer.writerow(row)
            
            print('svg_no=',svg_no,'cns dta=',split_h[6],cnsdat,'data len text and svg=',len(db_data.description),len(svg_data.svg_tags))
            
            for cns in cnsdat:
                rec=cns.split(',')
                reclen=len(rec)
                reject=''
                if(cns!='' and reclen!=2):
                    reject='cnsvg reject'
                    print('cnsvg data len=',reclen,rec,reject)
                
                if(cns!='' and reclen==2):
                    cnsvg_data=My_CnSvg.objects.get(pk=rec[1])
                    my_no=db_data.no
                    no=cnsvg_data.no
                    kind='My_CnSvg'
                    dfg=cnsvg_data.dfg
                    data_0=cnsvg_data.svg_tags
                    data_1=''
                    data_2=''                        
                    row = []
                    row += [my_no, no, kind, dfg, data_0, data_1, data_2]
                    cnsvg_data_rec+=1
                    writer.writerow(row)
        print('my_data nn=',my_data_rec,'svg_data nn=',svg_data_rec,'cnsvg_data nn=',cnsvg_data_rec)

    return HttpResponse('complete!')
# ------------------------------------------------------------------
def sql_reject_parms(request,parm):
    from datetime import date
    import csv
    global parm_len
    
    if(parm=='none'):
        parm_len=0
    else:
        parms=parm.split(':')
        set_len=len(parms)
        print('parm=',parm,'parms=',parms,'leng=',len(parms))
        if(set_len<1):
            print('parms wrong!!')
            exit()
        else:
            set_key=[]
            for pm in parms:
                keys=pm.split(',')
                if keys[-1] == '':
                    keys.pop()
                if(keys[0]==''):
                    continue
                else:
                    set_key.append(keys)
            print('set_key=',set_key)
            if(len(set_key)==0):
                print('parms wrong!!')
                exit()
            
    t = date.today()
    output_path = './'
    output_name = t.strftime('%Y%m%d') + '_mysql_movedata.csv'
    
    # CSV出力処理開始
    #f = open(wfile,'w',encoding='cp932',newline="")
    with open(output_path + output_name, 'w', encoding='utf-8', newline='') as csv_file:
    #codecs.open(file_path, 'r', 'utf-8', 'ignore') as file:
    #with codecs.open(output_path + output_name, 'w', 'cp932','ignore') as csv_file:
        # 1行目にヘッダーを書き込む
        header = ['My_no', 'no', 'kind', 'del', 'data_0', 'data_1', 'data_2']
        #writer = csv.writer(csv_file, delimiter='\t', quoting=csv.QUOTE_ALL)
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        
        # 検索対象レコードの抽出
        list = My_Sys.objects.only("no","kind","dfg").all().order_by("no")
        #list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

        sys_data_rec=0
        for dat in list:
            db_data = My_Sys.objects.get(pk=dat.id)     
        #for kk in list:
            #db_data = My_Sys.objects.get(pk=kk)
            my_no=db_data.no
            no=db_data.no
            kind='My_Sys'
            dfg=db_data.dfg
            data_0=db_data.description
            data_1=''
            data_2=''
            
            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            sys_data_rec+=1
            writer.writerow(row)
            
            print('My_Sys num ,id, my_no=',sys_data_rec,db_data.id,my_no,'kind=',kind,'del flg=',dfg,data_0)
                    
        # 検索対象レコードの抽出
        list = My_Data.objects.only("no","kind","dfg").all().order_by("no")
        
        my_data_rec=0
        svg_data_rec=0
        cnsvg_data_rec=0
        for dat in list:
            db_data = My_Data.objects.get(pk=dat.no)
            my_no=db_data.no
            no=db_data.no
            kind='My_Data'
            d_key=[db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3]
            result=False
            for keys in set_key:
                result=match_key_pattern(keys,d_key)
                print('My Data matching=',result,'keys=',keys,'d_keys=',d_key)
                if(result==True):
                    break
            dfg=db_data.dfg
            if(result==True):
                dfg=result
            #header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            data_0=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            #overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            data_1=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            #view_tex=db_data.description
            data_2=db_data.description

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            my_data_rec+=1
            writer.writerow(row)
            print('my_data num ,id, my_no==',my_data_rec,db_data.id,my_no,'kind=',kind,'dfg=',dfg,'data_0=',data_0)
            
            split_h=data_0.split('|<=>|')
            svg_no=split_h[4]
            cnsdat=split_h[6].split(';')
            
            #Top svgデータの読み込みとcsvへのwrite
            svg_data=My_Svg.objects.get(pk=svg_no)
            my_no=db_data.no
            no=svg_data.no
            kind='My_Svg'
            dfg=svg_data.dfg
            data_0=svg_data.svg_tags
            data_1=''
            data_2=''

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            svg_data_rec+=1
            writer.writerow(row)
            
            print('svg_no num ,id, my_no==',svg_data_rec,svg_data.id,no,svg_no,'cns dta=',split_h[6],cnsdat,'data len text and svg=',len(db_data.description),len(svg_data.svg_tags))
            
            for cns in cnsdat:
                rec=cns.split(',')
                reclen=len(rec)
                reject=''
                if(cns!='' and reclen!=2):
                    reject='cnsvg reject'
                    print('cnsvg data len=',reclen,rec,reject)
                
                if(cns!='' and reclen==2):
                    cnsvg_data=My_CnSvg.objects.get(pk=rec[1])
                    my_no=db_data.no
                    no=cnsvg_data.no
                    kind='My_CnSvg'
                    dfg=cnsvg_data.dfg
                    data_0=cnsvg_data.svg_tags
                    data_1=''
                    data_2=''                        
                    row = []
                    row += [my_no, no, kind, dfg, data_0, data_1, data_2]
                    cnsvg_data_rec+=1
                    writer.writerow(row)
        print('my_data nn=',my_data_rec,'svg_data nn=',svg_data_rec,'cnsvg_data nn=',cnsvg_data_rec)

    return HttpResponse('complete!')
# ------------------------------------------------------------------
def sql_extract_parms(request,parm):
    from datetime import date
    import csv
    global parm_len
    
    if(parm=='none'):
        parm_len=0
    else:
        parms=parm.split(':')
        set_len=len(parms)
        print('parm=',parm,'parms=',parms,'leng=',len(parms))
        if(set_len<1):
            print('parms wrong!!')
            exit()
        else:
            set_key=[]
            for pm in parms:
                keys=pm.split(',')
                if keys[-1] == '':
                    keys.pop()
                if(keys[0]==''):
                    continue
                else:
                    set_key.append(keys)
            print('set_key=',set_key)
            if(len(set_key)==0):
                print('parms wrong!!')
                exit()
            
    t = date.today()
    output_path = './'
    output_name = t.strftime('%Y%m%d') + '_mysql_movedata.csv'
    
    # CSV出力処理開始
    #f = open(wfile,'w',encoding='cp932',newline="")
    with open(output_path + output_name, 'w', encoding='utf-8', newline='') as csv_file:
    #codecs.open(file_path, 'r', 'utf-8', 'ignore') as file:
    #with codecs.open(output_path + output_name, 'w', 'cp932','ignore') as csv_file:
        # 1行目にヘッダーを書き込む
        header = ['My_no', 'no', 'kind', 'del', 'data_0', 'data_1', 'data_2']
        #writer = csv.writer(csv_file, delimiter='\t', quoting=csv.QUOTE_ALL)
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        
        # 検索対象レコードの抽出
        list = My_Sys.objects.only("no","kind","dfg").all().order_by("no")
        #list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

        sys_data_rec=0
        for dat in list:
            db_data = My_Sys.objects.get(pk=dat.id)
        #for kk in list:
            #db_data = My_Sys.objects.get(pk=kk)
            my_no=db_data.no
            no=db_data.no
            kind='My_Sys'
            dfg=db_data.dfg
            data_0=db_data.description
            data_1=''
            data_2=''
            
            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            sys_data_rec+=1
            writer.writerow(row)
            
            print('My_Sys num=',sys_data_rec,my_no,'kind=',kind,'del flg=',dfg,data_0)
                    
        # 検索対象レコードの抽出
        list = My_Data.objects.only("no","kind","dfg").all().order_by("no")
        
        my_data_rec=0
        svg_data_rec=0
        cnsvg_data_rec=0
        for dat in list:
            db_data = My_Data.objects.get(pk=dat.no)
            my_no=db_data.no
            no=db_data.no
            kind='My_Data'
            d_key=[db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3]
            result=False
            for keys in set_key:
                result=match_key_pattern(keys,d_key)
                print('My Data matching=',result,'keys=',keys,'d_keys=',d_key)
                if(result==True):
                    break
            dfg=True
            if(result==True):
                dfg=False
            if(db_data.dfg==True):
                dfg=True
            #header=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            data_0=my_header(db_data.no,db_data.kind,db_data.dfg,db_data.mfg,db_data.svg_no,db_data.cnsvg_nums,db_data.cnsvg_tags)
            #overviews=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            data_1=my_overviews(db_data.theme,db_data.bunrui1,db_data.bunrui2,db_data.bunrui3,db_data.day_regist,db_data.day_modify,db_data.author,db_data.overview,db_data.keywords)
            #view_tex=db_data.description
            data_2=db_data.description

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            my_data_rec+=1
            writer.writerow(row)
            print('my_data=',my_no,'kind=',kind,'dfg=',dfg,'data_0=',data_0)
            
            split_h=data_0.split('|<=>|')
            svg_no=split_h[4]
            cnsdat=split_h[6].split(';')
            
            #Top svgデータの読み込みとcsvへのwrite
            svg_data=My_Svg.objects.get(pk=svg_no)
            my_no=db_data.no
            no=svg_data.no
            kind='My_Svg'
            dfg=svg_data.dfg
            data_0=svg_data.svg_tags
            data_1=''
            data_2=''

            row = []
            row += [my_no, no, kind, dfg, data_0, data_1, data_2]
            svg_data_rec+=1
            writer.writerow(row)
            
            print('svg_no=',svg_no,'cns dta=',split_h[6],cnsdat,'data len text and svg=',len(db_data.description),len(svg_data.svg_tags))
            
            for cns in cnsdat:
                rec=cns.split(',')
                reclen=len(rec)
                reject=''
                if(cns!='' and reclen!=2):
                    reject='cnsvg reject'
                    print('cnsvg data len=',reclen,rec,reject)
                
                if(cns!='' and reclen==2):
                    cnsvg_data=My_CnSvg.objects.get(pk=rec[1])
                    my_no=db_data.no
                    no=cnsvg_data.no
                    kind='My_CnSvg'
                    dfg=cnsvg_data.dfg
                    data_0=cnsvg_data.svg_tags
                    data_1=''
                    data_2=''                        
                    row = []
                    row += [my_no, no, kind, dfg, data_0, data_1, data_2]
                    cnsvg_data_rec+=1
                    writer.writerow(row)
        print('my_data nn=',my_data_rec,'svg_data nn=',svg_data_rec,'cnsvg_data nn=',cnsvg_data_rec)

    return HttpResponse('complete!')
# ------------------------------------------------------------------
def match_key_pattern(keys,d_key):
    ln=len(keys)
    result=True
    for k in range(ln):
        print('key_match k=',k,(keys[k]==d_key[k]),'key=',keys[k],d_key[k])
        if(keys[k]!=d_key[k]):
            result=False
            break  
    return result
#
# ------------------------------------------------------------------
def match_key(keys,key):
    ln=len(keys)
    result=-1
    for k in range(ln):
        if(keys[k]==key):
            result=k
            break
    
    return result
#
# ------------------------------------------------------------------
def tags_compose(keys,nums,nn):
    conct=''
    ln=len(keys)
    if(ln!=len(nums)):
        #print('*****Index Key length Error')
        exit()
    for k in range(ln):
        conct=conct+keys[k]+','+str(nums[k])+','+str(nn[k])
        #print(str(nums[k]))
        if(k<ln-1):
            conct=conct+'|<=>|'
    return conct
#
# ------------------------------------------------------------------
def tags_decompose(tags):
    keys=[]
    nums=[]
    nn=[]
    #print('**at decompose tags=',tags)
    if(tags==''):
        return keys,nums,nn
    spltchar=tags.split('|<=>|')
    ln=len(spltchar)

    for k in range(ln):
        nsp=spltchar[k].rfind(',')
        fst=spltchar[k][:nsp]
        snd=spltchar[k][nsp+1:]
        #print('org=',spltchar[k],' fst,snd=',fst,snd)
        nn.append(int(snd))
        nsp2=fst.rfind(',')
        keys.append(fst[:nsp2])
        lst=fst[nsp2+1:]
        #print('fst,lst=',fst[:nsp2],lst)
        nums.append(int(lst))   
    
    return keys,nums,nn
#
# ------------------------------------------------------------------
def recs_compose(nums):
    conct=''
    ln=len(nums)
    for k in range(ln):
        conct=conct+str(nums[k])
        #print(str(nums[k]))
        if(k<ln-1):
            conct=conct+','
    return conct
#
# ------------------------------------------------------------------
def recs_decompose(tags):
    
    spltchar=tags.split(',;')  
    
    return spltchar
#
# ------------------------------------------------------------------
def handle_uploaded_file(file_obj):
    sys.stderr.write("*** handle_uploaded_file *** aaa ***\n")
    sys.stderr.write(file_obj.name + "\n")
    file_path = 'media/documents/' + file_obj.name 
    sys.stderr.write(file_path + "\n")
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            sys.stderr.write("*** handle_uploaded_file *** ccc ***\n")
            #destination.write(chunk.decode())
            destination.write(chunk)
            sys.stderr.write("*** handle_uploaded_file *** eee ***\n")
        return file_path
"""
    with open(file_path, 'w',encoding='utf-8') as destination:
        # read csv
        rdr = csv.reader(destination)
        # ignore header
        #next(rdr)
        # upsert
        ncnt=0
        for r in rdr:        
            ncnt=ncnt+1
            print('count= '+str(ncnt)+' theme= '+r[0]+' bunrui1= '+r[1])
"""
#
# ------------------------------------------------------------------
def prepare_system(request):
### make system record 0 to 9: 10items
    global db_data,svg_data
    """
    ixdata.kind='Ind'
    ixdata.mfg = False
    ixdata.level= 0
    ixdata.rec_num= 0
    ixdata.key_num= 0
    ixdata.key_tags = ''    
    """
    ixdata_0 = My_Index.objects.create()
    ixdata_0.no=ixdata_0.pk
    ixdata_0.kind='Ind'
    ixdata_0.mfg = False
    ixdata_0.level= 0
    ixdata_0.rec_num= 0
    ixdata_0.key_nums= 0
    ixdata_0.key_tags = ''
    print('Index0_rec pk=',ixdata_0.pk)
    ixdata_1 = My_Index.objects.create()
    ixdata_1.no=ixdata_1.pk
    ixdata_1.kind='Ind'
    ixdata_1.mfg = False
    ixdata_1.level= 1
    ixdata_1.rec_num= 0
    ixdata_1.key_nums= 0
    ixdata_1.key_tags = ''
    print('Index1_rec pk=',ixdata_1.pk)
    ixdata_2 = My_Index.objects.create()
    ixdata_2.no=ixdata_2.pk
    ixdata_2.kind='Ind'
    ixdata_2.mfg = False
    ixdata_2.level= 2
    ixdata_2.rec_num= 0
    ixdata_2.key_nums= 0
    ixdata_2.key_tags = ''
    print('Index2_rec pk=',ixdata_2.pk)
    ixdata_3 = My_Index.objects.create()
    ixdata_3.no=ixdata_3.pk
    ixdata_3.kind='Ind'
    ixdata_3.mfg = False
    ixdata_3.level= 3
    ixdata_3.rec_num= 0
    ixdata_3.key_nums= 0
    ixdata_3.key_tags=''
    print('Index3_rec pk=',ixdata_3.pk)
    
    """
    recs_data = My_Recs.objects.create()
    recs_data.no=recs_data.pk
    recs_data.kind='Recs'
    recs_data.mfg = False
    recs_data.rec_num=0
    recs_data.tags=''
    recs_data.save()
    print('Recs_rec pk=',recs_data.pk)
    keys=['']
    points=[recs_data.pk]
    tags=tags_compose(keys,points)
    ixdata_3.key_tags = tags
    """
    
    ixdata_3.save()
    keys=['']
    points=[ixdata_3.pk]
    nn=[0]
    tags=tags_compose(keys,points,nn)
    ixdata_2.key_tags = tags
    ixdata_2.save()
    points=[ixdata_2.pk]
    tags=tags_compose(keys,points,nn)
    ixdata_1.key_tags = tags
    ixdata_1.save()
    points=[ixdata_1.pk]
    tags=tags_compose(keys,points,nn)
    ixdata_0.key_tags = tags
    ixdata_0.save()
    
    #print('recs_data',recs_data,recs_data.tags)
    print('ixdata_3',ixdata_3,ixdata_3.key_tags)
    print('ixdata_2',ixdata_2,ixdata_2.key_tags)
    print('ixdata_1',ixdata_1,ixdata_1.key_tags)
    print('ixdata_0',ixdata_0,ixdata_0.key_tags)
        
    #data_id = request.GET.get("rec_number")
    for data_id in range(1,50):
        #data = My_Data.objects.get(pk=data_id)
        data=My_Sys.objects.create()
        npk=data.pk
        print("rec_number= ",data_id," data=",data,'pk=',npk)
        #svg_data=My_Svg.objects.get(pk=data.svg_no)

        desc=''
        for k in range(0,1000):
            desc=desc+str(random.randint(0,9))

        #print("length=",len(desc)," record=",desc)

        data.kind="Sys"
        data.theme="system"
        data.bunrui1=""
        data.bunrui2=""
        data.bunrui3=""
        data.overview=""
        data.description=desc
        data.save()

    return HttpResponse('system prepared!')
#
# ------------------------------------------------------------------
def save_all(request):
    global db_data,svg_data
    # 適切な CSV 用ヘッダとともに HttpResponse オブジェクトを生成します。
    #response = HttpResponse(mimetype='text/csv')
    #response['Content-Disposition'] = 'attachment; filename=sqlite_dump.csv'
    #writer = csv.writer(response)

    wfile = 'media/documents/' + 'save_all.csv'

    print('file_path= ',wfile)
    f = open(wfile,'w',encoding='cp932',newline="")
    writer = csv.writer(f)

    result = My_Data.objects.all().order_by('no')
    print('records = ',result.count())

    for data in result:
        print("rec_number= ",data.no," data=",data)
        svg_data=My_Svg.objects.get(pk=data.svg_no)

        rec=[data.theme,data.bunrui1,data.bunrui2,data.bunrui3,data.day_regist,data.day_modify,data.overview,data.description,data.keywords]
        print('rec=',rec)
        writer.writerow(rec)

        if(svg_data.svg_tags!=""):
            rec=["","","","svg",svg_data.svg_tags]
            print('rec=',rec)
            writer.writerow(rec)

    return HttpResponse('all data write to csv!')
#
# ------------------------------------------------------------------
def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。
    ページングしたい場合に利用してください。
    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。
        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}
    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。
    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj
# ------------------------------------------------------------------
def get_page(request):
    #mydata_list = My_Data.objects.values("theme","bunrui1","overview").all()
    mydata_list = My_Data.objects.only("no","theme","bunrui1","bunrui2","bunrui3","day_regist","overview").all()
    #print('my_data_list type=',type(mydata_list));
    for data in mydata_list:
        g1=str(data.no)
        g2=data.theme
        g3=data.bunrui2
        g4=data.overview
        #print(g1,g2,g3,g4)

    page_obj = paginate_queryset(request, mydata_list, 20)
    #print('**page obj=',type(page_obj),len(page_obj),page_obj.object_list)
    #tex = request.GET.get("message")
    #print("**get_page** recieve "+ tex);
    #                my.overview = decode(line[6])
    #            my.description = decode(line[7])
    
    context = {
        'page_list': page_obj.object_list,
        'page_obj': page_obj,
    }
    return render(request, 'db_serv/page_list.html', context)
# ------------------------------------------------------------------
def get_index(request):
    global mydata_org
    global mydata_list
    global mydata
    
    global recs_data
    global ixdata_3
    global ixdata_2
    global ixdata_1
    global ixdata_0
    
    global Srch_level
    global Srch_prev_level
    global Srch_key
    global Srch_prev_key
    global Srch_v0_pkn
    global Srch_v0_key
    global Srch_v1_pkn
    global Srch_v1_key
    global Srch_v2_pkn
    global Srch_v2_key
    global Srch_v3_pkn
    global Srch_v3_key

    level = request.GET.get("level")
    pk_num = request.GET.get("pk_num")
    key_wd= request.GET.get("key_wd")
    #info('***Get_index level='+level+' pk_num='+pk_num+' key_wd='+key_wd)
    Srch_prev_key=Srch_key
    Srch_key=key_wd
    
    if (key_wd=='課題名' and int(level)>=1):
        level='0'
        Srch_v0_pkn=0
        Srch_v0_key=''
    if (key_wd=='大分類' and int(level)>=2):
        level='1'
        pk_num=Srch_v0_pkn
        key_wd=Srch_v0_key
    if (key_wd=='中分類' and int(level)>=3):
        level='2'
        pk_num=Srch_v1_pkn
        key_wd=Srch_v1_key
#    if (key_wd=='小分類' and int(level)>=4):
#        level='3'
#        pk_num=Srch_v1_pkn
#        key_wd=Srch_v1_key
        #print('set level=',level)
        
    if(level=='0'):
        #ixdata_0 = My_Index.objects.get(pk=1)
        ixdata_0 = My_Index.objects.get(pk=1)
        level=ixdata_0.level
        rec_num=ixdata_0.rec_num
        key_nums=ixdata_0.key_nums
        key_tags=ixdata_0.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v0_pkn=0
        Srch_v0_key=''
    
    if(level=='1'):
        ixdata_1 = My_Index.objects.get(pk=pk_num)
        level=ixdata_1.level
        rec_num=ixdata_1.rec_num
        key_nums=ixdata_1.key_nums
        key_tags=ixdata_1.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v0_pkn=pk_num
        Srch_v0_key=key_wd        
        
    if(level=='2'):
        ixdata_2 = My_Index.objects.get(pk=pk_num)
        level=ixdata_2.level
        rec_num=ixdata_2.rec_num
        key_nums=ixdata_2.key_nums
        key_tags=ixdata_2.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v1_pkn=pk_num
        Srch_v1_key=key_wd
        
    if(level=='3'):
        ixdata_3 = My_Index.objects.get(pk=pk_num)
        level=ixdata_3.level
        rec_num=ixdata_3.rec_num
        key_nums=ixdata_3.key_nums
        key_tags=ixdata_3.key_tags
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v2_pkn=pk_num
        Srch_v2_key=key_wd
        
    if(level=='4'):
        level=4
        rec_num=0
        key_nums=0
        key_tags=''
        #print('level=',level,' rec_num=',rec_num,' key_nums=',key_nums)
        Srch_prev_level=Srch_level
        Srch_level=level
        Srch_v3_pkn=0
        Srch_v3_key=key_wd

    context = {
        'level':level,
        'rec_num':rec_num,
        'key_nums':key_nums,
        'key_tags':key_tags,
    }
    
    return JsonResponse(context)
# ------------------------------------------------------------------
def success(request):
    str_out = "Success!<p />"

    return HttpResponse(str_out)
# ------------------------------------------------------------------
def encode(source):
    new_source = ''

    for char in source:
        if ord(char) in codepoint2name:
            char = '&%s;' % codepoint2name[ord(char)]
        new_source =new_source+ char

    return new_source
# ------------------------------------------------------------------
def decode(source):

    for entitie in re.findall('&(?:[a-z][a-z0-9]+);', source):
        entitie = entitie.replace('&', '')
        entitie = entitie.replace(';', '')
        source = source.replace('&%s;' % entitie, unichr(name2codepoint[entitie]))
        #source = source.replace('&%s;' % entitie, chr(name2codepoint[entitie]))

    return source
# -----------------------------------------------------------------
"""
def mail_to(request):
    from django.core.mail import EmailMessage
    #from django.core.mail import EmailMultiAlternatives
    
    doc_type = request.GET.get("type")
    html_dat = request.GET.get("html_dat")
    title = request.GET.get("title")
    
    print(doc_type,title,html_dat)
    fp = open('templates/db_serv/mail_template/sample.html','w',encoding='utf-8')
    fp.write(html_dat)
    fp.close()

    # 表題
    subject = title
    # 送信元
    from_email = "yzr.sonoda@gmail.com"
    #from_email = "yzr_sonoda24@yahoo.co.jp"
    # 送信先
    recipient_list = [
        "yzr_sonoda24@yahoo.co.jp","yzr.sonoda@gmail.com",
    ]
    
    text_content = '添付のsample.htmlを御覧下さい。'
    #msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    mail = EmailMessage(subject, text_content, from_email, recipient_list)
    #msg.attach_alternative(sample, "text/html")
    #mail.attach('templates/db_serv/mail_template/sample.html')
    mail.attach_file('templates/db_serv/mail_template/sample.html')
    #msg.send()
    mail.send()
    
    return HttpResponse('mail success')
"""
# ------------------------------------------------------------------
def display(request):
    return render(request, 'db_serv/display.html')
# ------------------------------------------------------------------
import logging
logger = logging.getLogger(__name__)
#import google.cloud.logging
#from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging

# クライアントのインスタンスを生成
#client = google.cloud.logging.Client()

# GCPのロギング ハンドラを作成
#handler = CloudLoggingHandler(client)

# GCPのロギングシステムの設定
#logging_format = '[%(levelname)s, %(name)s], %(message)s'
#formatter = logging.Formatter(logging_format)
#handler.setFormatter(formatter)
#setup_logging(handler, log_level=logging.INFO) # デフォルトはINFO
logging.basicConfig(level=logging.INFO)
def info(msg):
    logger.info('info '+msg)
#def debug(msg):
#    logger = logging.getLogger('command')
#    logging.debug('debug '+msg)
