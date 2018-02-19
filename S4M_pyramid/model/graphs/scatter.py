from .graph import *
class Scatterplot_Graph(Graph):
    def __init__ (self,Graph_Data,sort_by):
        #super(Graph, self).__init__()
        self.graph_data = Graph_Data
        self.graph_type = "scatter"
        self.sort_by = sort_by
        self._calculate_grouped_graph_data(sort_by)
        self._create_data_for_flot()
        self.x_axis_ticks = []





        
    """
    This converts the values currently held into data for flot in the javascript.

    There are two types of options - one with Sample type and one without. 

    For the one using Sample Type, a for each by probe in the grouped_graph_data, 
    there is another for each on the sample type display order (from the annotations) 
    and all the samples are kept in order in sample_ids variable for that sample type.

    Then the samples are sorted and then a for each is done on the sorted sample
    ids for that sample type and the xaxis is calculated and the values assigned.

    For the non-Sample Type option, the for each by probe on grouped_graph data is the
    same. The second for each is simply on whatever was the next level of the 
    grouped_graph_data. 

    These loops can be replaced with a function before sample_id in sample_ids for loop.

    """
    def _create_data_for_flot(self):     #CRITICAL-1 - DONE
        sampleTypeDisplayOrder = self.graph_data.ds_md['sampleTypeDisplayOrder'].split(",")
        markings = {}

        xaxis_labels = {}

        number_of_probes = len(self.grouped_graph_data)
        number_of_sample_types = len(sampleTypeDisplayOrder)
        scatter_color_array = self.get_scatter_color_array()
        number_of_scatter_colors = len(scatter_color_array)

        
        plot_data = {}
        plot_data_sd = {}
        probe_color_dict = {}
        probe_count = 0
        sort_by = self.sort_by
        try:
            for probe_id in self.grouped_graph_data:

                plot_data[probe_id] = []
                plot_data_sd[probe_id] = []
                try:
                    probe_color = scatter_color_array[probe_count]
                except:
                    # if it goes over the number of colours, then re-use the colors
                    level = probe_count / number_of_scatter_colors
                    color_reuse = probe_count - level * number_of_scatter_colors
                    probe_color = scatter_color_array[color_reuse]

                display_probe_id = self.return_renamed_probe(probe_id)
                probe_color_dict[probe_id] = {'color':probe_color,'display_probe_id':display_probe_id}

                count_points = 1 # want the very first point at 1
                sample_type_count = 0
                if sort_by == 'Sample Type':


                    """
                    Here we are splitting the samples up by sample type so that we can calculate their 
                    position on the x axis after sorting samples alphabetically.
                    """
                    for sample_type in sampleTypeDisplayOrder:
                        sample_type_order_of_display = sampleTypeDisplayOrder.index(sample_type) + 1
                        start_count_points = count_points
                        sample_ids = []
                        for sample_id in self.grouped_graph_data[probe_id][sample_type]['points']: 
                            sample_ids.append(sample_id)
                        sample_ids.sort() 

                        """ This is the same process except using 'sample_type' as below and can be refactored"""
                        for sample_id in sample_ids: #CRITICAL-4 
                            xaxis = count_points 
                            expression_value = self.grouped_graph_data[probe_id][sample_type]['points'][sample_id]['expression_value']

                            sd = self.grouped_graph_data[probe_id][sample_type]['points'][sample_id]['standard_deviation']

                            # add in sample id and sd into plot_data for easy use in displaying table
                            plot_data[probe_id].append([xaxis,expression_value,sample_id,sd,probe_color]) 

                            if expression_value is None:
                                sd_high = None
                                sd_low = None
                            else:
                                sd_high =expression_value+sd 
                                sd_low =expression_value-sd 

                            plot_data_sd[probe_id].append([[xaxis,sd_high],[xaxis,sd_low]]) 

                            count_points += 1

                        markings[sample_type_count] = {}
                        markings[sample_type_count]['color'] = '#666'
                        markings[sample_type_count]['lineWidth'] = 1
                        markings[sample_type_count]['xaxis'] = {}
                        markings[sample_type_count]['xaxis']['from'] = count_points - 0.5
                        markings[sample_type_count]['xaxis']['to'] = count_points - 0.5 


                        xaxis_label_position = float(start_count_points + count_points - 1) / 2 
                        xaxis_labels[sample_type] = {'level':1,'type':'Non-probe','name':sample_type,'xaxis_position': xaxis_label_position }
                        sample_type_count +=1
                else:
                    """
                    Here we are splitting the samples up by the first sort by type so that we can calculate their 
                    position on the x axis after sorting samples alphabetically.
                    """
                    for sort_by_type in self.grouped_graph_data[probe_id]:
                        start_count_points = count_points
                        sample_ids = []
                        for sample_id in self.grouped_graph_data[probe_id][sort_by_type]['points']: 
                            sample_ids.append(sample_id)
                        sample_ids.sort() 
                        """ This is the same process except using 'sort_by_type' as above and can be refactored """
                        for sample_id in sample_ids:  #CRITICAL-4 
                            xaxis = count_points 
                            expression_value = self.grouped_graph_data[probe_id][sort_by_type]['points'][sample_id]['expression_value']

                            sd = self.grouped_graph_data[probe_id][sort_by_type]['points'][sample_id]['standard_deviation']

                            # add in sample id and sd into plot_data for easy use in displaying table
                            plot_data[probe_id].append([xaxis,expression_value,sample_id,sd]) 

                            if expression_value is None:
                                sd_high = None
                                sd_low = None
                            else:
                                sd_high =expression_value+sd 
                                sd_low =expression_value-sd 

                            plot_data_sd[probe_id].append([[xaxis,sd_high],[xaxis,sd_low]]) 

                            count_points += 1

                        markings[sample_type_count] = {}
                        markings[sample_type_count]['color'] = '#666'
                        markings[sample_type_count]['lineWidth'] = 1
                        markings[sample_type_count]['xaxis'] = {}
                        markings[sample_type_count]['xaxis']['from'] = count_points - 0.5
                        markings[sample_type_count]['xaxis']['to'] = count_points - 0.5 


                        xaxis_label_position = float(start_count_points + count_points - 1) / 2 
                        xaxis_labels[sort_by_type] = {'level':1,'type':'Non-probe','name':sort_by_type,'xaxis_position': xaxis_label_position }
                        sample_type_count +=1

                setMax = count_points - 0.5

                # remove the last markings as it is not needed
                del markings[sample_type_count - 1]

                probe_count +=1

            self.max_x_axis = len(self.graph_data.sample_labels) + 0.5
        except:
            self.max_x_axis = 0
            pass


        self.markings = markings 
        self.plot_data = plot_data
        self.xaxis_labels = xaxis_labels
        self.plot_data_sd = plot_data_sd
        self.probe_color_dict = probe_color_dict
        self.min_x_axis = 0.5

