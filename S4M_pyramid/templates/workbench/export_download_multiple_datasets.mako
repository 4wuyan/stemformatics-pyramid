<%
    try:
        filter_ds_ids = []
        temp_filter_ds_ids = c.ds_ids.split(',')
        for ds_id in temp_filter_ds_ids:
            filter_ds_ids.append(int(ds_id))
    except:
        filter_ds_ids = None

    if c.export_type == 'datasets':
        row_list = ['ds_id','handle','title','organism','samples found','all_samples']
        return_data = "\t".join(row_list) + "\n"
        for ds_id in c.data['datasets']:
            if filter_ds_ids is not None and ds_id not in filter_ds_ids:
                continue

            row_list = []
            row_list.append(str(ds_id))
            row_list.append(c.data['datasets'][ds_id]['handle'])
            row_list.append(c.data['datasets'][ds_id]['title'])
            row_list.append(c.data['datasets'][ds_id]['organism'])
            row_list.append(str(len(c.all_samples_by_ds_id[ds_id])))
            row_list.append(str(c.data['datasets'][ds_id]['number_of_samples']))
            row = "\t".join(row_list) + "\n"
            return_data  += row       
    if c.export_type =='samples':
        row_list = ['ds_id','handle','chip_id','sample_id','sample_type']
        return_data = "\t".join(row_list) + "\n"
        all_samples_by_ds_id = c.data['all_samples_by_ds_id']
        for ds_id in c.data['datasets']:
            if filter_ds_ids is not None and ds_id not in filter_ds_ids:
                continue
            for sample in all_samples_by_ds_id[ds_id]:
                row_list = []
                row_list.append(str(ds_id))
                row_list.append(c.data['datasets'][ds_id]['handle'])
                chip_type = sample[0]
                chip_id = sample[1]
                metadata_values = c.all_sample_metadata[chip_type][chip_id][ds_id]
                row_list.append(sample[1])
                row_list.append(metadata_values['Replicate Group ID'])
                row_list.append(metadata_values['Sample Type'])
                row = "\t".join(row_list) + "\n"
                return_data +=row
    if c.export_type == 'download_script':
        
        url_yugene_download = h.url('/datasets/download_yugene/',qualified=True) 
        url_gct_download = h.url('/datasets/download_gct/',qualified=True) 
        username = c.user
        return_data = "#!/bin/bash\n"
        for ds_id in c.data['datasets']:
            if filter_ds_ids is not None and ds_id not in filter_ds_ids:
                continue
            return_data += "wget \""+url_yugene_download+str(ds_id)+"?username="+username+"&export_key="+c.export_key+"\" -O "+ str(ds_id) + "_" + c.data['datasets'][ds_id]['handle']+ ".yugene.txt\n"
            return_data += "wget \""+url_gct_download+str(ds_id)+"?username="+username+"&export_key="+c.export_key+"\" -O "+ str(ds_id) + "_" + c.data['datasets'][ds_id]['handle']+ ".gct\n"
%>
${return_data}

