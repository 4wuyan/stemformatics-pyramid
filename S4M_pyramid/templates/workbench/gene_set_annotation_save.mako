<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">   
    <link rel="stylesheet" type="text/css" href="${h.url('/css/workbench/save_gene_set.css')}" >
</%def>

    

    <div id="wb_background" class="wb_background_divs">    
        <div id="wb_background_inner_div">
            
            ${Base.wb_breadcrumbs()}      
                
            <div class="wb_question_groups_selected">
                
                <div class="wb_main_menu_expanded">
                    <div class="wb_sub_menu_container">

                        
                        
                        <div class="wb_sub_menu wb_menu_items">
                            <div class="wb_sub_menu_inner_div">
                                New Gene List Details
                            </div>
                        </div>
                        <div class="wb_help_bar wb_menu_items">
                            <div class="wb_help_bar_inner_div">
                                Show help information
                            </div>
                        </div>
                        <div class="wb_help wb_menu_items">
                            <div class="wb_help_inner_div">                
                                <p>Save your new gene list name and description here.</p>
                            </div>
                            
                        </div>
                        
                    </div>
                    <div class="clear"></div>
                </div>
            
            </div>    
            
            <div id="form" class="tables">
                <div class="innerDiv">
        
                    <form action="${c.url}" method="post"> 
                      <dl> 
                        
                        % if c.message != "":
                        <dt><span class=warning>${c.message}</span></dt> 
                        % endif
                        <dt>Gene List Name:</dt> 
                        <dd><input type="text" name="gene_set_name" value="${c.gene_set_name}"></dd> 
                        <dt>Gene List Description:</dt> 
                        <dd><textarea class="wide" name="description">${c.description}</textarea></dd> 
                        <dt>
                          <input type="submit" name="authform" value="Save" /> 
                        </dt> 
                        <dd>
                        </dd> 
                      </dl> 
                      <div class="clear"></div>
                    </form>
                    
                </div>
            </div>

        
            
        </div>
    </div>
    

