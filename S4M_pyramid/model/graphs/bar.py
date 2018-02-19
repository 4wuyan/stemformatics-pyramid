from graph import *
import json 
import numpy
class TempData(object):
    pass

class Bar_Graph(Graph):
    def __init__ (self,Graph_Data,sort_by):
        #super(Graph, self).__init__()
        self.graph_data = Graph_Data
        self.graph_type = "bar"
        self.sort_by = sort_by
        self.x_axis_ticks = []

        # inherited
        self._calculate_grouped_graph_data(sort_by)

        #calculated here 
        self._create_data_for_flot()


    def _create_data_for_flot(self):    
        # Temporary object to store things in before calculating
        self._temp = TempData()
        self._temp.sampleTypeDisplayOrder = self.graph_data.ds_md['sampleTypeDisplayOrder'].split(",")
        self._temp.sampleTypeDisplayGroups = json.loads(self.graph_data.ds_md['sampleTypeDisplayGroups'])
        self._temp.sampleTypeDisplayGroupColours = self.return_sample_type_display_group_colours(self._temp.sampleTypeDisplayGroups)
        self._temp.markings = {}

        self._temp.xaxis_labels = {}
        self._temp.plot_data = {}

        try:
            if self.data_levels == 2:
                self._initialise_values_for_two_levels()
            if self.data_levels == 3:
                self._initialise_values_for_three_levels()
            self._temp.probe_count = 0
            self._temp.xaxis_labels_count = 0

            # go through each probe
            for self._temp.probe_id in self.graph_data.probe_list:
                if self._temp.probe_id not in self.grouped_graph_data:
                    continue

                ####################### Normal #########################3
                if self.data_levels ==2:
                    self._calculate_plot_data_for_two_levels()

                ####################### Group By Disease etc. #########################3
                if self.data_levels ==3:
                    self._calculate_plot_data_for_three_levels()
         
                self._temp.probe_count +=1

            self.markings = self._temp.markings 
            self.plot_data = self._temp.plot_data
            self.xaxis_labels = self._temp.xaxis_labels
            self.min_x_axis = 0
            self.max_x_axis = self.graph_data.number_of_probes*self._temp.total_length_of_one_probe_including_dividers ;
        except:
            pass

    ######################## Three levels is the Disease State etc ################################3
    def _initialise_values_for_three_levels(self):
        self._temp.number_of_sample_types = len(self._temp.sampleTypeDisplayOrder)
        self._temp.total_length_of_one_probe_including_dividers = self._calculate_total_length_for_one_probe_including_dividers_and_xaxis_positions_for_one_probe()
        self._calculate_markings()

    # Only in use for three levels
    def _calculate_total_length_for_one_probe_including_dividers_and_xaxis_positions_for_one_probe(self):
        # Just go through one probe id and get all the variations
        probe_id = self.graph_data.probe_list[0]
        counter =0
        counter_dict = {}
        first_group_list = []
        for first_group in self.grouped_graph_data[probe_id]:
            first_group_list.append(first_group)
            
        first_group_list.sort(key=unicode.lower)
        # Three levels, first level is Disease and second is Sample type
        for first_group in first_group_list:
            
            for second_group in self._temp.sampleTypeDisplayOrder:
                if second_group in self.grouped_graph_data[probe_id][first_group]:
                    counter +=1 
                    counter_dict[first_group+'|'+second_group] = counter
            counter +=1 
        self._temp.xaxis_positions = counter_dict
        return counter 

    def _calculate_plot_data_for_three_levels(self):
        scatter_color_array = self.get_scatter_color_array()
        self._calculate_probe_label_info()
        display_probe_id = self.return_renamed_probe(self._temp.probe_id)
         
        self._temp.xaxis_labels[self._temp.xaxis_labels_count] = {'level':2,'type':'Probe','id':self._temp.probe_id,'name':display_probe_id,'xaxis_position': self._temp.xaxis_label_position }
        self._temp.xaxis_labels_count += 1 
        
        ####### Go through first group by value (eg Disease) and then Second (sample type) #############
        for self._temp.first_group_by_value in self.grouped_graph_data[self._temp.probe_id]:

            for self._temp.second_group_by_value in self.grouped_graph_data[self._temp.probe_id][self._temp.first_group_by_value]:
                self._calculations_for_three_levels_second_group_by_value()

    # This is for three levels
    def _calculations_for_three_levels_second_group_by_value(self):

        if self._temp.second_group_by_value not in self.grouped_graph_data[self._temp.probe_id][self._temp.first_group_by_value]:
            return

        combined_identifier = self._temp.first_group_by_value + '|' + self._temp.second_group_by_value
        xaxis = self._temp.xaxis_positions[combined_identifier] + self._temp.probe_count * self._temp.total_length_of_one_probe_including_dividers
        row = self.grouped_graph_data[self._temp.probe_id][self._temp.first_group_by_value][self._temp.second_group_by_value]
        extra_info = row['extra_info'] 
        statistics = row['statistics'] 
        self._temp.identifier_xaxis_labels = self._temp.first_group_by_value+'|'+self._temp.probe_id
        if self._temp.identifier_xaxis_labels not in self._temp.xaxis_labels:
            self._temp.xaxis_labels[self._temp.identifier_xaxis_labels] = {'level':1,'type':'Non-probe','name':self._temp.first_group_by_value,'min': xaxis,'max':xaxis,'xaxis_position': xaxis}
            self._temp.xaxis_labels_count += 1 
        else:
            current_min = self._temp.xaxis_labels[self._temp.identifier_xaxis_labels]['min']
            current_max = self._temp.xaxis_labels[self._temp.identifier_xaxis_labels]['max']
            if xaxis < current_min:
                self._temp.xaxis_labels[self._temp.identifier_xaxis_labels]['min'] = xaxis
                current_min = xaxis
            if xaxis > current_max:
                self._temp.xaxis_labels[self._temp.identifier_xaxis_labels]['max'] = xaxis
                current_max = xaxis
            x_pos = numpy.mean([current_max,current_min])
            self._temp.xaxis_labels[self._temp.identifier_xaxis_labels]['xaxis_position'] = x_pos
             

        #Set ID to be probe|disease
        identifier = self._temp.probe_id+'|'+self._temp.second_group_by_value
        if identifier not in self._temp.plot_data:
            group_number = self._temp.sampleTypeDisplayGroups[self._temp.second_group_by_value]
            color = self._temp.sampleTypeDisplayGroupColours[group_number][0]
            self._temp.plot_data[identifier] = {}
            self._temp.plot_data[identifier]['values'] = {}
            self._temp.plot_data[identifier]['color'] = color 

        new_count = len(self._temp.plot_data[identifier]['values']) 
        self._temp.plot_data[identifier]['values'][new_count] = {}
        self._temp.plot_data[identifier]['values'][new_count]['average'] = statistics['Average']
        self._temp.plot_data[identifier]['values'][new_count]['max'] = statistics['Max']
        self._temp.plot_data[identifier]['values'][new_count]['min'] = statistics['Min']
        self._temp.plot_data[identifier]['values'][new_count]['median'] = statistics['Median']
        self._temp.plot_data[identifier]['values'][new_count]['sd'] = statistics['StandardDeviation']
        self._temp.plot_data[identifier]['values'][new_count]['Q1'] = statistics['Q1']
        self._temp.plot_data[identifier]['values'][new_count]['Q3'] = statistics['Q3']
        self._temp.plot_data[identifier]['values'][new_count]['level_above'] = self._temp.first_group_by_value
        self._temp.plot_data[identifier]['values'][new_count]['extra_info'] = extra_info
        self._temp.plot_data[identifier]['values'][new_count]['xaxis'] = xaxis 




    ######################## Two levels is the normal sample Type ################################3
    def _initialise_values_for_two_levels(self):
        self._temp.number_of_sample_types = len(self._temp.sampleTypeDisplayOrder)
        self._temp.total_length_of_one_probe_including_dividers = self._temp.number_of_sample_types + 1
        self._calculate_markings()

 
    def _calculate_plot_data_for_two_levels(self):
        sample_type_color_selected = {}
        self._calculate_probe_label_info()
        display_probe_id = self.return_renamed_probe(self._temp.probe_id)
        self._temp.xaxis_labels[self._temp.xaxis_labels_count] = {'level':1,'type':'Probe','id':self._temp.probe_id,'name':display_probe_id,'xaxis_position': self._temp.xaxis_label_position }
        self._temp.xaxis_labels_count += 1 

        for sample_type in self.grouped_graph_data[self._temp.probe_id]:
            identifier = sample_type
            if identifier not in self._temp.plot_data:
                self._temp.plot_data[identifier] = {}
                self._temp.plot_data[identifier]['values'] = {}

            sample_type_order_of_display = self._temp.sampleTypeDisplayOrder.index(sample_type) + 1
            xaxis = sample_type_order_of_display + self._temp.probe_count * self._temp.total_length_of_one_probe_including_dividers 

            new_count = len(self._temp.plot_data[identifier]['values']) 
            statistics = self.grouped_graph_data[self._temp.probe_id][sample_type]['statistics'] 
            extra_info = self.grouped_graph_data[self._temp.probe_id][sample_type]['extra_info'] 
            self._temp.plot_data[identifier]['values'][new_count] = {}
            self._temp.plot_data[identifier]['values'][new_count]['average'] = statistics['Average']
            self._temp.plot_data[identifier]['values'][new_count]['max'] = statistics['Max']
            self._temp.plot_data[identifier]['values'][new_count]['min'] = statistics['Min']
            self._temp.plot_data[identifier]['values'][new_count]['median'] = statistics['Median']
            self._temp.plot_data[identifier]['values'][new_count]['sd'] = statistics['StandardDeviation']
            self._temp.plot_data[identifier]['values'][new_count]['Q1'] = statistics['Q1']
            self._temp.plot_data[identifier]['values'][new_count]['Q3'] = statistics['Q3']
            self._temp.plot_data[identifier]['values'][new_count]['level_above'] = self._temp.probe_id
            self._temp.plot_data[identifier]['values'][new_count]['extra_info'] = extra_info
            self._temp.plot_data[identifier]['values'][new_count]['xaxis'] = xaxis 


        for sample_type in self._temp.sampleTypeDisplayOrder: 
            group_number = self._temp.sampleTypeDisplayGroups[sample_type]
            if group_number not in sample_type_color_selected:
                sample_type_color_selected[group_number] = 0
            current_group_colour_count = sample_type_color_selected[group_number]
            sample_type_color = self._temp.sampleTypeDisplayGroupColours[group_number][current_group_colour_count]
            sample_type_color_selected[group_number] += 1 
            self._temp.plot_data[sample_type]['color'] = sample_type_color 

    def _calculate_probe_label_info(self):
        start_of_probe = self._temp.probe_count * self._temp.total_length_of_one_probe_including_dividers + 1
        end_of_probe_without_dividers = start_of_probe + self._temp.total_length_of_one_probe_including_dividers - 2
        self._temp.xaxis_label_position = numpy.mean([start_of_probe,end_of_probe_without_dividers])


    def _calculate_markings(self):
        self._temp.number_of_vertical_line_dividers = self.graph_data.number_of_probes - 1
        for i in range(self._temp.number_of_vertical_line_dividers):
            array_count = i 
            real_count = i + 1
            x_axis = real_count*(self._temp.total_length_of_one_probe_including_dividers) 
            self._temp.markings[array_count] = {}
            self._temp.markings[array_count]['color'] = '#666'
            self._temp.markings[array_count]['lineWidth'] = 1
            self._temp.markings[array_count]['xaxis'] = {}
            self._temp.markings[array_count]['xaxis']['from'] = x_axis 
            self._temp.markings[array_count]['xaxis']['to'] = x_axis 

class Histogram_Graph(Bar_Graph):
    pass


class Box_Graph(Bar_Graph):
    def __init__ (self,Graph_Data,sort_by):
        super(Box_Graph, self).__init__(Graph_Data,sort_by)
        self.graph_type = "box"

