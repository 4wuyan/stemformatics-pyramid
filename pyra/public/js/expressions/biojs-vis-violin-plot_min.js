var biojsvisviolingraph;module.exports=biojsvisviolingraph=function(a){sort_x_by_probe_and_sample_type=function(c){options=c.options;var b=c.options.sortByOption.split(",");if(options.probe_order!=="none"){if(b.length!=1){sample_type_order=options.sample_type_order;probe_order=options.probe_order;nested_values=d3.nest().key(function(e){return e.Probe}).sortKeys(function(e,d){return probe_order.indexOf(e)-probe_order.indexOf(d)}).key(function(f){var e=b[0];return f[e]}).key(function(f){var e=b[1];return f[e]}).sortKeys(function(e,d){return sample_type_order.indexOf(e)-sample_type_order.indexOf(d)}).entries(options.data)}else{if(b[0]!="Sample_Type"){probe_order=options.probe_order;nested_values=d3.nest().key(function(e){return e.Probe}).sortKeys(function(e,d){return probe_order.indexOf(e)-probe_order.indexOf(d)}).key(function(f){var e=options.sortByOption;return f[e]}).entries(options.data)}else{sample_type_order=options.sample_type_order;probe_order=options.probe_order;nested_values=d3.nest().key(function(e){return e.Probe}).sortKeys(function(e,d){return probe_order.indexOf(e)-probe_order.indexOf(d)}).key(function(e){return e.Sample_Type}).sortKeys(function(e,d){return sample_type_order.indexOf(e)-sample_type_order.indexOf(d)}).entries(options.data)}}}else{if(options.multi_option!=1){nested_values=d3.nest().key(function(e){return e.Probe}).sortKeys(function(e,d){return probe_order.indexOf(e)-probe_order.indexOf(d)}).key(function(f){var e=b[0];return f[e]}).key(function(f){var e=b[1];return f[e]})}else{nested_values=d3.nest().key(function(e){return e.Probe}).key(function(e){return e[b[0]]}).entries(options.data)}}c.nested_values=nested_values;return c};setup_line_graph=function(c){sample_types_with_colour={};shrink_radius=false;options=c.options;probe_size=c.size_of_probe_collumn;sample_type_size=c.size_of_sample_type_collumn;nested_values=c.nested_values;line_group_list=[];sample_type_list=[];violin_data_array={};violin_path_array_min={};violin_path_array_max={};for(var A=0;A<options.probe_list.length;A++){violin_data_array[options.probe_list[A]]={};violin_path_array_min[options.probe_list[A]]={};violin_path_array_max[options.probe_list[A]]={};for(var D=0;D<options.sample_type_order.split(",").length;D++){var y=options.sample_type_order.split(",")[D];violin_data_array[options.probe_list[A]][y]=[];violin_path_array_min[options.probe_list[A]][y]=[];violin_path_array_max[options.probe_list[A]][y]=[]}}probe=null;line_groups=null;legend_name_array=[];var z=20;var h=c.multi_scaleX;var E;var n=options.sortByOption.split(",");var t=n[0];var q=[];if(options.multi_group!=1){t=n[1]}var G=c.name_mapping;for(A=0;A<nested_values.length;A++){for(k=0;k<nested_values[A].values.length;k++){if($.inArray(nested_values[A].values[k].key,sample_type_list)==-1){sample_type_list.push(nested_values[A].values[k].key)}}}for(probe in nested_values){g=nested_values[probe];values=g.values;var d=g.key;probe_num=parseInt(probe);violin_data_array[d]={};violin_path_array_min[d]={};violin_path_array_max[d]={};if(options.multi_group!=1){for(var D in values){g=values[D];u=g.values;m=g.key;number_secondary_groups=u.length;violin_data_array[d][m]={};violin_path_array_min[d][m]={};violin_path_array_max[d][m]={};for(var v in u){A=parseInt(v);r=u[A];secondary_grouping=r.values;e=r.key;number_samples=secondary_grouping.length;violin_data_array[d][m][e]=[];violin_path_array_max[d][m][e]=[];violin_path_array_min[d][m][e]=[];var H=h(G[remove_chars(d+"-"+e+"-"+m)]);if(A!=0){var f=u[A-1];var w=h(G[remove_chars(d+"-"+f.key+"-"+m)])}else{var w=0}if(A!=number_secondary_groups-1){var C=u[A+1];var B=h(G[remove_chars(d+"-"+C.key+"-"+m)])}else{B=options.width}sample_type_list=[];for(var o in secondary_grouping){if((secondary_grouping[o].Expression_Value==secondary_grouping[o].Expression_Value)&&((secondary_grouping[o].Expression_Value).toString()!=dataset_data.detectionThreshold)){q.push(secondary_grouping[o]);sample_type_list.push(secondary_grouping[o][t])}}w=H-(H-w)/2;B=H+(B-H)/2;if(q.length!=0){c=setup_scatter_line(c,probe_num,H,q,d,e,w,B,t,m)}}}for(var D in values){var g=values[D];var u=g.values;var m=g.key;for(var v in u){var A=parseInt(v);var r=u[A];var e=r.key;add_scatter_and_path(d,e,m)}}}else{for(line_groups in values){var m="";if($.inArray(values[line_groups].key,legend_name_array)==-1){legend_name_array.push(values[line_groups].key)}l=values[line_groups];q=l.values;new_samples=[];var H=h(G[remove_chars(d+"-"+q[0][t])]);for(D=0;D<q.length;D++){if((q[D].Expression_Value==q[D].Expression_Value)&&((q[D].Expression_Value).toString()!=dataset_data.detectionThreshold)){new_samples.push(q[D])}}b=l.key;for(A=0;A<legend_name_array.length;A++){if(!sample_types_with_colour[legend_name_array[A]]){sample_types_with_colour[legend_name_array[A]]=options.colour[colour_count];if(colour_count<options.colour.length){colour_count++}else{colour_count=0}}}if(line_groups!=0){var F=h(G[remove_chars(d+"-"+q[0][t])]);var w=h(G[remove_chars(d+"-"+values[parseInt(line_groups)-1].key)])}else{w=0}if(line_groups!=values.length-1){var B=h(G[remove_chars(d+"-"+values[parseInt(line_groups)+1].key)])}else{B=options.width-z}w=H-(H-w)/2;B=H+(B-H)/2;violin_data_array[d][b]=[];violin_path_array_min[d][b]=[];violin_path_array_max[d][b]=[];if(new_samples.length!=0){c=setup_scatter_line(c,probe_num,H,new_samples,d,b,w,B,t,m)}}for(line_groups in values){var l=values[line_groups];var q=l.values;var b=l.key;add_scatter_and_path(d,b,m)}}}c.line_group_list=line_group_list;return c};add_scatter_and_path=function(g,b,e){if(shrink_radius==true){radius=options.radius*estimated_shrink}if(options.multi_group==1){var f=violin_data_array[g][b];var d=violin_path_array_min[g][b];var h=violin_path_array_max[g][b]}else{var f=violin_data_array[g][e][b];var d=violin_path_array_min[g][e][b];var h=violin_path_array_max[g][e][b]}if((options.sortByOption.split(",")[0]=="Sample_Type"||options.sortByOption.split(",")[1]=="Sample_Type")){colour=options.colour}else{colour=options.colour_array}for(var c=0;c<f.length;c++){svg=add_scatter(f[c]["interpolate_min_values"],f[c]["interpolate_max_values"],f[c]["current_samples"],f[c]["graph"],f[c]["colour"],f[c]["centreX"],0,f[c]["tooltip"],f[c]["sample_count"],f[c]["min"],f[c]["max"],b,g,e)}(d).sort(function(l,j){return l.y-j.y});(h).sort(function(l,j){return l.y-j.y});svg.append("path").attr("d",line(d)).attr("stroke",colour[b]).style("stroke-width",options.stroke_width).style("fill","none");svg.append("path").attr("d",line(h)).attr("stroke",colour[b]).style("stroke-width",options.stroke_width).style("fill","none")};add_scatter_for_sample_ids=function(b,e,f,d){options=e.options;radius=options.radius;svg=e.svg;scaleY=e.scaleY;tooltip=options.tooltip;svg.call(tooltip);probe_count=0;var c=e.multi_axis_scale;svg.selectAll(".dot").data(b).enter().append("circle").attr("class",function(g){return"sample-type-"+g.LineGraphGroup}).attr("r",radius).attr("cx",function(h){var g=d(h.Replicate_ID);return g}).attr("cy",function(g){var h=0;h=scaleY(g.Expression_Value);return h}).style("stroke",options.background_stroke_colour).style("stroke-width","1px").style("fill",function(g){return options.colour_array[g.Sample_Type]}).attr("opacity",0.8).on("mouseover",tooltip.show).on("mouseout",tooltip.hide);e.svg=svg;return e};add_scatter=function(t,j,g,d,n,u,p,b,q,r,s,o,l,m){options=d.options;svg=d.svg;scaleY=d.scaleY;svg.call(b);var e=u;toggle_count_odd=1;toggle_count_even=0;var h=0;var f=0;var c=s;svg.selectAll(".dot").data(g).enter().append("circle").attr("id",function(v){return v.Replicate_ID}).attr("class",function(v){return"sample-type-"+v.LineGraphGroup}).attr("cx",function(w,v){if(w.Expression_Value==w.Expression_Value){if(v%2===0){h=e+(radius*toggle_count_even);f=h;toggle_count_even++}else{if(v%2===1){h=e-(radius*toggle_count_odd);c=h;toggle_count_odd++}}return h}else{return}}).attr("r",function(v){if(v.Expression_Value==v.Expression_Value){return radius}else{return 0}}).attr("cy",function(v){var w=0;if(p===0){if(v.Expression_Value==v.Expression_Value){w=scaleY(v.Expression_Value)}else{return}}else{w=scaleY(p)}return w}).style("stroke",options.background_stroke_colour).style("stroke-width","1px").style("fill",function(v){return n}).attr("opacity",0.8).on("mouseover",b.show).on("mouseout",b.hide);if(g.length>1){len=g.length-1;temp1={x:e-(radius*toggle_count_odd)-(radius*2),y:scaleY(g[len].Expression_Value)};t.push(temp1);temp2={x:e+(radius*toggle_count_odd)+(radius*2),y:scaleY(g[len].Expression_Value)};j.push(temp2);if(options.multi_group!=1){violin_path_array_min[l][m][o].push(temp1);violin_path_array_max[l][m][o].push(temp2)}else{violin_path_array_min[l][o].push(temp1);violin_path_array_max[l][o].push(temp2)}}return svg};setup_scatter_line=function(m,b,g,c,d,e,f,j,n,l){options=m.options;radius=options.radius;samples=c;scaleY=m.scaleY;radius=options.radius;max_samples=(options.width/(options.probe_count*options.sample_type_count))/options.radius;tooltip=make_scatter_tooltip(d,e,l,n);interpolate_min_values=[];interpolate_max_values=[];colour={};if((options.sortByOption.split(",")[0]=="Sample_Type"||options.sortByOption.split(",")[1]=="Sample_Type")){colour=options.colour[e]}else{colour=options.colour_array[e]}var h=g;rad=options.level_of_overlap;if(rad>options.y_axis_largest_value){rad=rad/200}current_samples=[];sample_count=0;c.sort(function(p,o){return p.Expression_Value-o.Expression_Value});lwr_l={x:h,y:scaleY(c[0].Expression_Value)+(2*radius)};interpolate_min_values.push(lwr_l);interpolate_max_values.push(lwr_l);final_diff=0;diff=0;if(c.length!=1){for(i=0;i<c.length;i++){current_samples.push(c[i]);if(i===c.length-1){diff+=Math.abs(c[i].Expression_Value-c[i-1].Expression_Value)}else{diff+=Math.abs(c[i].Expression_Value-c[i+1].Expression_Value)}if(diff<rad){sample_count++}else{if(diff>(2*rad)){if(i===c.length-1){yval=c[i].Expression_Value;final_diff=diff}else{yval=c[i+1].Expression_Value}tmp={x:h,y:scaleY(yval)-(diff/2)};interpolate_min_values.push(tmp);interpolate_max_values.push(tmp)}if(current_samples.length>max_samples){shrink_radius=true;if(estimated_shrink==0){estimated_shrink=max_samples/current_samples.length;prev_estimated_shrink=estimated_shrink}else{if(prev_estimated_shrink>(max_samples/current_samples.length)){estimated_shrink=max_samples/current_samples.length;prev_estimated_shrink=estimated_shrink}else{estimated_shrink=prev_estimated_shrink}}}violin_data={};violin_data.interpolate_min_values=interpolate_min_values;violin_data.interpolate_max_values=interpolate_max_values;violin_data.current_samples=current_samples;violin_data.graph=m;violin_data.colour=colour;violin_data.centreX=h;violin_data.tooltip=tooltip;violin_data.sample_count=sample_count;violin_data.min=f;violin_data.max=j;if(options.multi_group!=1){violin_data_array[d][l][e].push(violin_data)}else{violin_data_array[d][e].push(violin_data)}current_samples=[];sample_count=0;diff=0}}}else{violin_data={};violin_data.interpolate_min_values=interpolate_min_values;violin_data.interpolate_max_values=interpolate_max_values;violin_data.current_samples=c;violin_data.graph=m;violin_data.colour=colour;violin_data.centreX=h;violin_data.tooltip=tooltip;violin_data.sample_count=sample_count;violin_data.min=f;violin_data.max=j;if(options.multi_group!=1){violin_data_array[d][l][e].push(violin_data)}else{violin_data_array[d][e].push(violin_data)}}len=c.length-1;line=d3.svg.line().x(function(o){return o.x}).y(function(o){return o.y}).interpolate("basis");upr_l={x:h,y:scaleY(c[len].Expression_Value-(final_diff))-(2*rad)};interpolate_min_values.push(upr_l);interpolate_max_values.push(upr_l);interpolate_min_values.sort(function(p,o){return p.y-o.y});interpolate_max_values.sort(function(p,o){return o.y-p.y});if(options.multi_group!=1){violin_path_array_min[d][l][e]=(interpolate_min_values);violin_path_array_max[d][l][e]=(interpolate_max_values)}else{violin_path_array_min[d][e]=(interpolate_min_values);violin_path_array_max[d][e]=(interpolate_max_values)}for(i in interpolate_max_values){interpolate_min_values.push(interpolate_max_values[i])}m.svg=svg;return m};make_scatter_tooltip=function(c,d,e,f){var b=d3.tip().attr("class","d3-tip").offset([0,+110]).html(function(h){var g=options.probe_name_for_tooltip;temp=g+": "+c+"<br/>";if((sortBy=="Sample_Type")||(sortBy=="Sample Type")||(options.sortByOption.split(",").length!=1)){temp=temp+"Sample Type: "+d+" ["+sample_type_hover[d]+"]"}if(options.sortByOption.split(",").length!=1){temp=temp+"State: "+e}return temp});return b};sort_by_sample_type=function(c,b){if(b!=="none"){c.sort(function(e,d){return b.indexOf(e.Sample_Type)-b.indexOf(d.Sample_Type)})}else{c.sort(function(e,d){return e.Sample_Type.localeCompare(d.Sample_Type)})}return c};add_scatter_for_multiple_reps=function(j,c,b,g,e,d,h){svg=j.svg;options=j.options;box_width=options.box_width;box_width_wiskers=box_width/2;scaleY=j.scaleY;var f=get_x_value(j,c[0]);bar_vals=calculate_error_bars_violin(c);var l="none";svg=add_vertical_line_to_box(options.stroke_width,f,bar_vals[0],bar_vals[2],svg,scaleY,b,l);svg=add_scatter(c,j,b,g,bar_vals[1],e,d,h);j.svg=svg;j.temp_y_val=bar_vals[1];return j};calculate_error_bars_violin=function(c){var d=[];x=0;for(i in c){d.push(c[i].Expression_Value)}var b=get_mean_value(d);sum=0;numbers_meaned=[];for(x in d){numbers_meaned.push(Math.abs(d[x]-b))}standard_deviation=get_mean_value(numbers_meaned);return[b-standard_deviation,b,b+standard_deviation]};get_type=function(b){return b};setup_graph=function(d){d.graph_type="Violin Graph";estimated_shrink=0;prev_estimated_shrink=0;options=d.options;var b=options.x_axis_label_padding;d=setup_margins(d);var c=".probe_text";var h=".probe-";var e=".sample_text";var g=".second_sort_by";var f=".sample-";d=setup_svg(d);if(options.sort_by_sample_id==="no"){d=sort_x_by_probe_and_sample_type(d)}if(options.include_sample_type_x_axis==="yes"&&options.display.x_axis_labels==="yes"){b=80}d=setup_x_axis(d,options.x_axis_list);d=setup_data_for_x_axis(d);if(options.display.x_axis_labels==="yes"){b=b-100;d=setup_x_axis_labels(d,null,b,c,h,1);d=setup_x_axis_labels(d,null,b,".hidden-probe_text",h,1);b=b+100;d=setup_x_axis_labels(d,null,b,e,h,3);if(options.sortByOption.split(",").length>1){b+=120;d=setup_x_axis_labels(d,null,b,g,f,2)}}d=setup_y_axis(d);d=setup_line_graph(d);if(options.display.vertical_lines==="yes"){d=setup_vertical_lines(d,options.legend_list)}d=setup_watermark(d);if(options.display.legend=="yes"){d=setup_D3_legend(d,options.legend_list)}if(options.display.horizontal_lines==="yes"){d=setup_horizontal_lines(d)}return d};init=function(b){var c=default_options();c=b;page_options={};var d={};d.options=c;d=preprocess_lines(d);d=setup_graph(d);var e=$(c.target);e.addClass("line_graph");svg=d.svg;c.test_graph=d};init(a)};