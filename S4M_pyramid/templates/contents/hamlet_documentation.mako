<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<%namespace name="Base" file="../base.mako"/>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
  
    ${Base.default_inclusions()}  
    
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Hamlet - Interactive Heatmap Tool</title>

    <link type="text/css" href="${h.url('/css/hamlet.css')}" rel="stylesheet" />	

    <style type="text/css">
    </style>
    
    <script type="text/javascript">
    </script>
    
  </head>
  <body>
    ${Base.header()}
  
    <div id="hamlet-container">
      <div id="hamlet-container-top">
	<table cellpadding="20">
	  <tr>
      
        <td>
	      <a href="http://hamlet.wehi.edu.au/main/index/about">
		<img src="${h.url('/images/Logo2011.gif')}" width="255" height="52" alt="Hamlet Logo" style="border: 0;" />
	      </a>
	    </td>
        
	    <td style="vertical-align:middle;">
	      <span id="hamlet-container-subtitle">
		interactive heatmap tool<br/>
		version 0.2.1
	      </span>
	    </td>
	    <td style="vertical-align:middle;">
	    </td>
	  </tr>
	</table>
      </div>

      <div id="hamlet-container-content">
	<div id="hamlet-container-tabs">

	  <%def name="inclusions()">

      <h2>About Hamlet</h2>
	  <p>Hamlet is an online application designed to help analyse datasets, manily by using  heatmaps. It can be used to visualize trends in the data,  or cluster the data, for example (see below for a list of main features). It is primarily targeted at users who are familiar with the data they wish to analyse but may not have experience in programming, hence being unable to take advantage of more advanced tools such as R. It has been developed by Nick Seidenman and Jarny Choi from the <a href="http://www.wehi.edu.au">Walter and Eliza Hall Institute</a> in Melbourne as a way of analysing microarray expression data. Its development is also supported by the <a href="http://www.stemformatics.org">${c.site_name}</a> project. The code, which is primarily written in python, is open source, and will become available online soon under BSD license.  For further information about Hamlet, please click <a href="http://hamlet.wehi.edu.au/main/index/about">here.</a></p>


	  <h2>Documentation Index</h2>
	  <ul> 
	    <li><a href="#terminology">Some Terminology </a>(rows and columns vs samples and probes)</li> 
	    <li><a href="#viewing">Viewing Heatmap</a> (basic heatmap view, zooming in, changing appearance)</li> 
	    <li><a href="#sorting">Sorting and Clustering</a> (finding correlated probes or samples, clustering all probes or samples)</li> 
	    <li><a href="#filtering">Filtering and Aggregating</a> (filtering, aggregating probes)</li> 
	    <li><a href="#faq">FAQ</a></li> 
	  </ul>

	  <h2><a name="terminology" id="terminology"></a>Some Terminology</h2>
	  <p>Hamlet often refers to its rows as 'samples' and and columns as 'probes'. This terminology comes from Hamlet's origin as a tool for microarray expression analysis, where a probe's expression profile is measured across a number of different samples. For example, rather than referring to clustering of rows, we may refer to clustering of samples. Even though we lose the reference to the specific orientation of the matrix this way, we can end up with easier to understand operations on the data in its context, hence this choice of words. Note however that 'samples' may also really mean 'cell types' or 'time points' or any other reference to the actual data. The sample microarray data available for selection, for example, hold profiles across various cell types, where for each cell type, aggregated averages across biological replicates have been calculated.</p>
	  <h2><a name="viewing" id="viewing"></a>Viewing Heatmap</h2>
	  <h3>Basic heatmap view</h3>
	  <p>After inputting data, either by copy and paste or by selecting a dataset, a heatmap is rendered immediately. Note that the heatmap shown is actually a rotated version of the copy and paste data input. This is largely a historical artifact which may be fixed in future versions, as we initially had some technical issues with rotations of certain labels over others. Note also that a histogram of values is displayed in the bottom left hand corner, with mean and median of the entire dataset also shown.</p>
	  <p>Note that not all row and column labels may be displayed, if there are too many to show. Instead of not showing any labels at all in this case, Hamlet displays labels at certain intervals, and these can change as you scale the heatmap. This behaviour is common to many scaling displays such as Google maps, which  show only certain street names at a particular scale of viewing and hide others. To get the actual row and column labels at a particular point of the heatmap, use the mouse-over which will create highlighted row and column labels.</p>
	  <p>The first display of the heatmap often may not look very interesting, depending on the distribution of values in the data, especially with microarray datasets where the majority of values are around the low &quot;not expressed&quot; values. This is why the initial rendering of the heatmap of the two provided datasets show mainly  blue tiles. It isn't until we start filtering and clustering, that we will start to see some interesting patterns in these cases.</p>
	  <h3>Zooming In</h3>
	  <p>One of the niftier features of Hamlet is the ability to select and zoom in on a subregion of a heatmap. The zoom function is invoked by first clicking on the &quot;Zoom&quot; button. A dialog that pops up will show two windows: probes and samples. This dialog will initially appear in the middle of the page, but you can move it by grabbing and dragging the title bar.</p>
	  <p>Select a region now by clicking and dragging the mouse. A rectangular region will become highlighted and at the same time, the probes and samples boxes in the dialog will begin to fill with names of probes and samples contained inside the highlighted area. When you release the mouse button, you'll see &quot;handles&quot; on the highlight box that will let you resize it in any direction. If you position the mouse somewhere over the middle of the box, you should see a &quot;hand&quot; pointer icon appear. This lets you know you can click and drag the box to a different location in the heatmap. As you move or resize the box, the probes and samples windows will be updated in real time. Once you're satisfied with your selection, click the OK button in the dialog box, and a new heatmap, zoomed in to this region, will be generated and should appear in a few seconds.</p>
	  <p>If you want to change the selection completely, you can click anywhere outside the selection box and then click-drag a new selection. Hitting the Cancel button will cancel the zoom mode.      </p>
	  <h3>Changing appearance</h3>
	  <p>You can customize the appearance of the heatmap by using the &quot;View&quot; button. Customization options available include selection of colours, adjusting the size of the font on the labels, and changing the range of colors used based on values in the dataset.</p>
	  <h2><a name="sorting" id="sorting"></a>Sorting and Clustering<br />
	  </h2>
	  <p>Clustering uses one of the selected distance measures between any two items to cluster the probes or the samples together. If there are missing values, the distance calculation will ignore the missing values as much as possible. For example, if sample clustering was being done and each sample had 5 values, but if one sample had 2  missing values, and another sample had no missing values, the distance measurement will be done on the 3 non-missing pairs. Note that clustering works on the data currently being shown, so if you've zoomed into an area, for example, the clustering will be done only for that area, and not for the entire dataset.</p>
	  <h3>Finding Correlated Probes or Samples</h3>
	  <p>You may be interested in finding all probes whose profiles are similar to a particular probe. This can be done using the &quot;Single Point&quot; tab after clicking on the &quot;Cluster&quot; button. By clicking on anywhere on the heatmap, you can see the reference point used. After clicking the OK button, clustering is done in real time and a new image will be displayed, where the reference point is always in the top left hand corner.</p>
	  <h3>Clustering All Probes or Samples</h3>
	  <p>All the probes and/or samples can be clustered. This is particularly useful for finding patterns in the data and a commonly used operation with heatmaps. This can be done using the &quot;Whole Dataset&quot; tab after clicking on the &quot;Cluster&quot; button.</p>
	  <h2><a name="filtering" id="filtering"></a>Filtering and Aggregating<br />
	  </h2>

	  <h3>Filtering</h3>
	  <p>You can filter out probes satisfying certain criteria. Value range filtering works by specifying minimum and maximum values within which the probe will be kept. For example, a probe with values of (3,2,2,5,6) will pass the filter and be included if (min,max) is set to (2,7), but will not pass the filter if (min,max) is set to (3,7) or (2,4). You can imagine the (min,max) value to be a sort of lower and upper bounds of a window you're setting, and only probes where all the sample values lie within the window will be kept after filtering.</p>
	  <p>Flatline threshold filtering works to try to reduce probes with little variation across the samples. So if this value is set to 1.0, and suppose the dataset has mean value of 5, then any probes where all the sample values lie within 1.0 standard deviation of 5 will be filtered out.</p>
	  <h3>Aggregating Probes</h3>
	  <p>Hamlet can aggregate  probes together (currently sample aggragation is not available). This is available under &quot;Tiles&quot; tab after clicking on the &quot;View&quot; button. How many probes it will aggregate together depends on the number of partitions chosen. For example, if there are 1000 probes, and you choose 100 partitions, 10 neighbouring probes will be aggregated together to form 1 probe. Several methods of aggregation are provided, including average, minimum and maximum. In general, you probably want to cluster the probes first, and then aggregate, to ensure that you're aggregating highly correlated neighbours together. Note that if there are more probes in the dataset being shown than there are pixels available to render colours for each probe, Hamlet automatically aggregates the values anyway.</p>

	  <h2><a name="faq" id="faq"></a>FAQ</h2>
	  <p><strong>What browsers are supported by Hamlet?</strong></p>
	  <p style="margin-top:0.5em;">Hamlet relies on <a href="http://jquery.com">jquery</a> javascript library,  hence browsers supported by jquery are also supported by Hamlet. See the full list <a href="http://docs.jquery.com/Browser_compatibility">here</a>.</p>
	  </%def>
	  ${inclusions()}
	</div>
      </div>
    </div>
    ${Base.footer()}  
  </body>
</html>
