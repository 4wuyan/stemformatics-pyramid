<%inherit file="/default.html"/>
<%namespace name="Base" file="/base.mako"/>

<%def name="includes()">
  <link rel="stylesheet" type="text/css" href="${h.url('/css/admin/troubleshoot_geg.css')}" >
</%def>
<div class="title">
  Troubleshooting GEG
</div>
</br>
% if hasattr(c, 'output'):
    <%
        output = c.output
        output = output.replace("%20", " ")
    %>
    <div class="title">
      ${output}
    </div>
% endif
<ul class="buttonMenus">
  <li id="exportMenu">
    <form id="deleteSTR_form" action="/admin/troubleshoot_geg?ds_id=${c.ds_id}&delete=yes" method="post">
      <input type="submit" name="deleteSTR" value="Delete GEG REDIS CACHE [Short Term Redis]">
    </form>
    <form id="refreshLTR_form" action="/admin/setup_new_dataset/${c.ds_id}" method="post" target="_blank">
      <input type="submit" name="RefreshLTR" value="Setup Dataset ${c.ds_id} in Redis [Long Term Redis] ">
    </form>
  </li>
</ul>
</br>

<div id="form">
<div class="innerDiv wb_help_inner_div info" >
<p>
  <span class="bold">Information:</span>
</p>
</br>
<p>
  In ${c.site_name}, we store the data (such as gct values, gene to probe mappings, probe graph data used in Gene Expression Graph, Yugene values) in redis so as to access it quickly instead of building it again and again.
</p>
</br>
<p>
  The data such as gene to probe mapping, gene list to gene mappings , probe graph data are stored in redis for ${c.expiry_time} hours. These are referred as <span class="bold">short tem redis cache</span>.
</p>
</br>
<p>
  The data such as gct values/yugene values are stored in redis, until they are explicitly deleted/refreshed by someone. These are referred as <span class="bold">long term redis cache</span>.
</p>
</br>
<p>
  <span class="bold">Commonly Faced Issues:</span>
</p>
<ul id="issues_list">
  <li> Graph not coming up on one of the production servers, while the same graph is working on other servers.</li>
  <li> Change in Sample IDs in dataset, which leads to different samples/values on same graph on different servers.</li>
  <li> Graph not coming up for a new mapping ID.</li>
</ul>
</br>
<p class="bold">
  All the above issues can be fixed by resetting Redis data (Short term/Long term).
</p>
</br>
<p>
  To clear Cache, please click on buttons provided above.
</p>

</div>
</div>
</br>
<div id="form">
<div class="wb_help_inner_div info" >
  <div class="result_title">
    Mapping Information
  </div>
  <p>
    Total Number of Mappings found for dataset ${c.ds_id} are <span class="bold">${c.count}</span>.
  </p>
  <p>
    Click <a href="/contents/download_mappings" class="link">here</a> to Download Mappings.
  </p>
  </div>
  </div>
</br>

<div id="form">
<div class="innerDiv">
  <div class="result_title">
    List of Short term Redis Keys found for GEG
  </div>
  % if c.result != {}:
    <table>
      <tbody>
        % for row in c.result[c.ds_id]:
        <tr>
          <td>
            ${row}
          </td>
        </tr>
        % endfor
      </tbody>
    </table>
  % else:
    <div class="">
      No data found
    </div>
  % endif
</div>


</div>
