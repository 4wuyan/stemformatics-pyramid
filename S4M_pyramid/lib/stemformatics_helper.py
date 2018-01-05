from webhelpers2.html import literal

"""
    Dictionary of pagination to use this
    {'next_page': 2, 'start_page': 1, 'prev_page': 1, 'start': 0, 'end': 50, 'total': 9906, 'page': 1, 'end_page': 199}
"""
def print_paginate(dict_paginate):

    html = ""


    # <span class="current">1</span> | <span><a href="/situations/admin/situations/index/page:2">2</a></span> | <span><a href="/situations/admin/situations/index/page:3">3</a></span> | <span><a href="/situations/admin/situations/index/page:4">4</a></span> | <span><a href="/situations/admin/situations/index/page:5">5</a></span>	<a href="/situations/admin/situations/index/page:2">next &gt;&gt;</a></div>
    page = dict_paginate['page']
    prev_page = dict_paginate['prev_page']
    start_page = dict_paginate['start_page']
    end_page = dict_paginate['end_page']
    next_page = dict_paginate['next_page']
    base_url = dict_paginate['base_url']
    order_by = dict_paginate['order_by']
    start = dict_paginate['start'] + 1
    end = dict_paginate['end']

    html = "<div class=\"paging\">"

    html = html + "<div class=\"show\"> Page "+str(page) +" of " + str(end_page) + " | Records " + str(start) + " to " + str(end) + "</div>"


    # previous option
    if page == start_page:
        html = html + "<div class=\"disabled\">&lt;&lt; previous</div>"
    else:
        html = html + "<div class=\"link\"><a class=basic_link href=\""+base_url+"&order_by="+order_by+"&page="+ str(prev_page) +"\">&lt;&lt; previous</a></div>"


    # select page #
    html = html + "<div class=\"select\"><select class=\"select_page\">"

    for i in range(start_page,end_page + 1 ):

        if i == page:
            html = html + "<option selected value=\""+ str(i) +"\">"+str(i)+"</option>"
        else:
            html = html + "<option value=\""+ str(i) +"\">"+str(i)+"</option>"

    html = html + "</select></div>"


    # next
    if page == end_page:
        html = html + "<div class=\"disabled\">next &gt;&gt;</div>"
    else:
        html = html + "<div class=\"link\"><a class=basic_link href=\""+base_url+"&order_by="+order_by+"&page="+ str(next_page) +"\">next &gt;&gt;</a></div>"




    html = html + "<div class=\"clear\"></div></div>"

    return literal(html)




def setup_accession_ids_for_viewing(dataset_metadata):

    ae_id = dataset_metadata['ae_accession_id']
    geo_id = dataset_metadata['geo_accession_id']
    sra_id = dataset_metadata['sra_accession_id']
    pxd_id = dataset_metadata['pxd_accession_id']
    ena_id = dataset_metadata['ena_accession_id']
    url_list = []

    if ae_id != 'N/A' and ae_id != 'NULL' and ae_id != '' :
        url_list.append('<a target="_blank" href="http://www.ebi.ac.uk/arrayexpress/experiments/' + ae_id+'">'+ae_id+'</a>')

    if geo_id != 'N/A' and geo_id != 'NULL' and geo_id != '' :
        url_list.append('<a target="_blank" href="http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + geo_id+'">'+geo_id+'</a>')

    if sra_id != 'N/A' and sra_id != 'NULL' and sra_id != '' :
        url_list.append('<a target="_blank" href="https://trace.ncbi.nlm.nih.gov/Traces/sra/?study=' + sra_id+'">'+sra_id+'</a>')

    if pxd_id != 'N/A' and pxd_id != 'NULL' and pxd_id != '' :
        url_list.append('<a target="_blank" href="http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=' + pxd_id+'">'+pxd_id+'</a>')

    if ena_id != 'N/A' and ena_id != 'NULL' and ena_id != '' :
        url_list.append('<a target="_blank" href="http://www.ebi.ac.uk/ena/data/view/' + ena_id+'">'+ena_id+'</a>')

    html = ' | '.join(url_list)


    return literal(html)


def get_citations(ds_id,citations):

    try:
        first_author =  citations[ds_id]['First Authors']
    except:
        first_author =  ""

    try:
        title =  citations[ds_id]['Publication Title']
    except:
        title = ""
    try:
        citation =  citations[ds_id]['Publication Citation']
    except:
        citation = ""

    ## replace DOI part with a link to DOI resolver
    doistart = citation.find('DOI:')
    if doistart > 0:
        doiparts = citation[doistart:].split(" ")
        doi = doiparts[1]
        citation = citation.replace(citation[doistart:], '<a href="http://dx.doi.org/'+doi+'" target="_blank">DOI: '+doi+'</a>')

    html = first_author+" <em style='font-style:italic'>et al.</em> "+title+" "+citation
    return literal(html)


def get_citations_part(ds_id,citations,key):
    try:
        citations_part = citations[ds_id][key]
    except:
        citations_part = ""

    return literal(citations_part)



def setup_email_to_contributing_author(dataset,ds_id,username,external_base_url):
    from guide.lib.stemformatics_helper import setup_accession_ids_for_viewing
    from pylons import url, config
    site_name = config['site_name']
    accession_url = setup_accession_ids_for_viewing(dataset)
    dataset_url = url('/datasets/search?ds_id='+str(ds_id),qualified=True)
    text = """
            Email to: %s
    <br/>
    <br/>
    <br/>
    <br/>
--------------------------------- <br/>
Australian Institute for Bioengineering and Nanotechnology (AIBN) <br/>
The University of Queensland <br/>
Brisbane Qld 4072 <br/>
Australia <br/>
http://www.aibn.uq.edu.au <br/>
http://www.stemformatics.org <br/>
contact: info@stemformatics.org <br/>
---------------------------------
    <br/>
    <br/>
            Dear Dr %s,
    <br/>
    <br/>
My name is %s, a member of the %s team, which is an academic platform which allows researchers to visually analyze and explore publicly available and exemplary mouse and human stem cell datasets. We are a community-driven resource - all of the experiments hosted by our database are curated by stem cell annotator and a computational curator and we only include data that meets high quality standards.
    <br/>
    <br/>
We are writing to let you know that we've included your study "%s" using the accession identifier %s and it is available for viewing at: %s. We've propagated all of the contact information available, but if you prefer us to change any of these details, then please let us know.
    <br/>
    <br/>
%s is a free resource which operates under an open access model. Datasets hosted by %s are indexed by the Web of Science. We are funded by the Australian Research Council to support the stem cell community to make use of exemplary stem cell datasets. We attribute all data directly back to data generators and authors with transparent links to the appropriate data repository (such as GEO) as well as the original publication via PubMed, and we include host lab information where possible.  We require %s users to cite the original publications describing the datasets hosted by %s where these are accessed from our platform. A description of the %s resource was published in 2013: Wells CA, et al Stemformatics: Visualisation and sharing of stem cell gene expression. Stem Cell Research 2013: 10(3) pp387-395  DOI dx.doi.org/10.1016/j.scr.2012.12.003.
    <br/>
    <br/>
Please feel free to contact myself, or the Project Manager, Rowland Mosbergen (info@stemformatics.org); or the lab head Christine Wells (c.wells@uq.edu.au) if you have any questions about how your data is hosted in %s, or if you have any suggestions for other datasets that you would like us to include.
    <br/>
    <br/>
    <br/>
    Best regards      """ % (dataset['email'],dataset['name'],username,site_name,dataset['title'],accession_url,dataset_url,site_name,site_name,site_name,site_name,site_name,site_name,)

    return text

def create_letter_for_annotator(ds_id,uid,user,handle,external_base_url):
    from pylons import config
    site_name = config['site_name']
    text = """
    Dear %s,
<br/>
<br/>
    I have imported your dataset '%s' into %s. It has some basic sample annotations to start you off but we need your help to get the dataset ready for use.
<br/>
<br/>
    We have noticed that the QC plots show that the clustering of the samples is not exactly what we would expect. I will ask Christine to have a look at them and she can then discuss with you any conclusions or suggestions she arrives at. I have attached a document containing the QC plots for your reference. This doesn't stop us from putting your dataset into %s as a private dataset for you.
<br/>
<br/>

    This dataset cannot be accessed publically, but I have given you access to this dataset as an annotator.  This access allows you to tailor the graphs the way you want and to provide details on the dataset summary page and the rest of the front end.
<br/>
<br/>
    Please make sure you are already logged into %s with the email address %s. If you haven't already signed up, you can register here:
<br/>
    %s/auth/register?username=%s
<br/>
<br/>

    Then you can access the current dataset summary page here:
<br/>
    %s/datasets/search?ds_id=%s
<br/>
<br/>

    You can access the annotator webpage for your dataset here:
<br/>
    %s/admin/annotate_dataset?ds_id=%s#
<br/>
<br/>

    First of all, have a look at the steps on the Control Bar. These will show you in what order you should annotate your dataset. Once you click on each step, have a read of the help at the top of the page and try to annotate the dataset yourself.
<br/>
<br/>

    After you have had a try, we can talk via Skype to answer any questions you have and to give me feedback on what part of the annotating was confusing and what was easy.  This allows us to improve our annotation page.
<br/>
<br/>

    Any problems, please let me know. Screenshots would be very helpful if you run into trouble.
        """ % (user.full_name,handle,site_name,site_name,site_name,user.username,external_base_url,user.username,external_base_url,str(ds_id),external_base_url,str(ds_id),)
    return text

def web_asset_url(relative_url):
    from pylons import url, config
    use_cdn = config['use_cdn']
    try:
        cdn_base_url = config['cdn_base_url']
    except:
        use_cdn = 'false'

    if use_cdn == 'true':
        final_url = "//"+cdn_base_url + relative_url
    else:
        final_url =  url(relative_url)


    return final_url

def external_dependency_url(external_url,fallback_url):
    # As of Sept 2017, stemformatics website requests will be served on https
    new_external_url = 'https://'+external_url

    from pylons import url, config
    use_cdn = config['use_cdn']

    try:
        cdn_base_url = config['cdn_base_url']
    except:
        use_cdn = 'false'

    if use_cdn == 'true':
        final_url = new_external_url
    else:
        final_url =  url(fallback_url)

    return final_url
