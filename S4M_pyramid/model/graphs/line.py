from .graph import *
import json 
class Line_Graph(Graph):

    def __init__ (self,Graph_Data,sort_by):
        self.graph_data = Graph_Data
        self.graph_type = "line"
        self.sort_by = "LineGraphGroup"
        self._calculate_grouped_graph_data(self.sort_by)
        self._create_data_for_flot()

    """
    This takes the data we have that is grouped by self.grouped_graph_data[day][lineGraphGroup]
    and creates all the values of the positions needed to display it in flot.

    The lineGraphOrdering is the annotated data that tells us the ordering of the day value.
    eg. if first_group_by_value is 'Day 0', then the lineGraphOrdering[first_group_by_value]
    might be set as 0. similarly 'Day 18', might have a value of 7. This is used to calculate 
    the x axis position within the probe.

    Initially get the markings - these are the vertical lines that separates probes 

    Then go through all the probes in the probe list and work out where on the xaxis they 
    should be shown as labels.

    Now we want to  go through each of the first group by (day) values and the second group by 
    (line graph group) values and work out their x axis position, based on the lineGraphOrdering 
    value and which probe this point is on. Also save the statistics calcualted earlier  into a 
    format that is ready for the javascript as well as the color selected and the xaxis position.
     
    Please note that it uses the scatter color array to pick the colors.

    xaxis_labels['full'] - this is the level that is the time part - eg. Day 0 or Hour 3
    xaxis_labels['summary'] - this is the probe level eg. Clec4e Probe 
    identifier - this is the probe id plus the lineGraphGroup value eg. ILMN_121525|High Dox

    plot_data[identifier]['values'][counter] is the data for the  plot going across the graph. 
    eg. all the plot points for ILMN_121525 with High Dox will be joined by lines across the page

    """
    def _create_data_for_flot(self):     #CRITICAL-1 - DONE
        lineGraphOrdering = json.loads(self.graph_data.ds_md['lineGraphOrdering'])
        markings = {}
        self.x_axis_ticks = []
        scatter_color_array = self.get_scatter_color_array()
        xaxis_labels = {}
        xaxis_labels['full'] = {}
        xaxis_labels['summary'] = {}

        number_of_probes = len(self.grouped_graph_data)
        number_of_sample_types = len(lineGraphOrdering)

        """ Setting up the vertical lines that separates probes """
        number_of_vertical_line_dividers = number_of_probes - 1
        total_length_of_one_probe_including_dividers = number_of_sample_types + 1
        setMax = number_of_probes * total_length_of_one_probe_including_dividers
        for i in range(number_of_vertical_line_dividers):
            array_count = i 
            real_count = i + 1
            x_axis = real_count*(total_length_of_one_probe_including_dividers) 
            markings[array_count] = {}
            markings[array_count]['color'] = '#666'
            markings[array_count]['lineWidth'] = 1
            markings[array_count]['xaxis'] = {}
            markings[array_count]['xaxis']['from'] = x_axis 
            markings[array_count]['xaxis']['to'] = x_axis 

        """ 
        two for eaches to start calculating the positions and other information ready
        for graphing with flot
        """
        plot_data = {}
        probe_count = 0
        xaxis_labels_count = 0
        xaxis_label_level_1_list = []
        for probe_id in self.graph_data.probe_list:
            try:
                graph_data_for_probe = self.grouped_graph_data[probe_id] 
            except:
                continue

            colour_number = 0
            start_of_probe = probe_count * total_length_of_one_probe_including_dividers + 1
            end_of_probe_with_dividers = start_of_probe + total_length_of_one_probe_including_dividers
            end_of_probe_without_dividers = start_of_probe + number_of_sample_types - 1
            xaxis_label_position = float(start_of_probe + end_of_probe_without_dividers) / 2 

            display_probe_id = self.return_renamed_probe(probe_id)
            xaxis_labels['full'][xaxis_labels_count] = {'level':2,'type':'Probe','id':probe_id,'name':display_probe_id,'xaxis_position': xaxis_label_position }
            xaxis_labels['summary'][xaxis_labels_count] = {'level':1,'type':'Probe','id':probe_id,'name':display_probe_id,'xaxis_position': xaxis_label_position }
            xaxis_labels_count += 1 

            list_of_first_group_by = []
            for first_group_by_value in graph_data_for_probe :
                list_of_first_group_by.append(first_group_by_value)
                first_group_by_value_order_of_display = lineGraphOrdering[first_group_by_value]
                xaxis = first_group_by_value_order_of_display + probe_count * total_length_of_one_probe_including_dividers 
                xaxis_labels['full'][xaxis_labels_count] = {'level':1,'type':'Non-probe','name':first_group_by_value,'xaxis_position': xaxis}
                xaxis_labels_count += 1 
                self.x_axis_ticks.append(xaxis)

                for second_group_by_value in self.grouped_graph_data[probe_id][first_group_by_value]:
                    statistics = self.grouped_graph_data[probe_id][first_group_by_value][second_group_by_value]['statistics'] 
                    identifier = probe_id+'|'+second_group_by_value

                    if identifier not in plot_data:
                        color = scatter_color_array[colour_number]
                        colour_number+=1 
                        plot_data[identifier] = {}
                        plot_data[identifier]['values'] = {}
                        plot_data[identifier]['color'] = color 

                    new_count = len(plot_data[identifier]['values']) 
                    plot_data[identifier]['values'][new_count] = {}
                    plot_data[identifier]['values'][new_count]['average'] = statistics['Average']
                    plot_data[identifier]['values'][new_count]['max'] = statistics['Max']
                    plot_data[identifier]['values'][new_count]['min'] = statistics['Min']
                    plot_data[identifier]['values'][new_count]['median'] = statistics['Median']
                    plot_data[identifier]['values'][new_count]['sd'] = statistics['StandardDeviation']
                    plot_data[identifier]['values'][new_count]['Q1'] = statistics['Q1']
                    plot_data[identifier]['values'][new_count]['Q3'] = statistics['Q3']
                    plot_data[identifier]['values'][new_count]['extra_info'] = ""
                    plot_data[identifier]['values'][new_count]['xaxis'] = xaxis 

 
            probe_count +=1

        self.markings = markings 
        self.plot_data = plot_data
        self.xaxis_labels = xaxis_labels
        self.min_x_axis = 0
        self.max_x_axis = self.graph_data.number_of_probes*(len(lineGraphOrdering) + 1);


