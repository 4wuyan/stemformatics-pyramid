<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">   
    <link type="text/css" href="${h.url('/css/workbench/index.css')}" rel="stylesheet" />
    <script type="text/javascript" src="${h.url('/js/workbench/index.js')}"></script>
</%def>

    ${Base.links()}  
    
    <div class="rightColumn">
    
        <div id="workbench">
        
            <div class="title"> Workbench for ${c.user} </div> <a href="${h.url('/contents/site_features_dataset_summary')}" class="linkButtons helpPopup">HELP &gt; </a>
            
            <div class="mainTextColumn content">
                <table id="geneList">
                    <thead>
                        <tr>
                            <th class="th1">5 Top Gene Lists</th>
                            
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>List #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                            
                        </tr>
                        <tr>
                            <td>List #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        <tr>
                            <td>List #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        <tr>
                            <td>Job #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        <tr>
                            <td>Job #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                    </tbody>
                </table>
    
            
                <table id="analysisList">
                    <thead>
                        <tr>
                            <th class="th1">5 Last Analysis Jobs</th>
                            <th>Actions</th>
                            
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Job #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        <tr>
                            <td>Job #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        <tr>
                            <td>Job #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        <tr>
                            <td>Job #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        <tr>
                            <td>Job #1</td>
                            <td><a href="#">Edit</a> | <a href="#">Delete</a></td>
                        </tr>
                        
                    </tbody>
                </table>
                
                
                
                <div class="clear"></div>                
                
            </div>
            
            
            <div class="dashboard content sideColumn">
            
                <div class="search"><a href="${h.url('/workbench/gene_list_view')}" class="">GENE LIST &gt;&gt;</a></div>
                <div class="search"><a href="${h.url('/workbench/gene_list_view')}" class="">ANALYSIS &gt;&gt;</a></div>
                <div class="search"><a href="${h.url('/auth/history/show')}" class="">HISTORY &gt;&gt;</a></div>
                <div class="search"><a href="${h.url('/auth/update_details')}" class="">SETTINGS &gt;&gt;</a></div>
                
                <div class="clear"></div>
                
            
            
            </div>
            

        </div>
    </div>
