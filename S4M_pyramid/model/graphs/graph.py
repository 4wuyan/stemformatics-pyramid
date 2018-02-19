import logging
log = logging.getLogger(__name__)
import redis
import sqlalchemy as SA
from sqlalchemy import or_, and_, desc

import numpy
from guide.model.stemformatics import *
import pylons
from pylons import config,app_globals as g


import math

class Graph(object):

    lowest_expression_value = None

    @staticmethod
    def get_scatter_color_array():
        return ['#7F6610','#000000','#6633CC','#00CC99','#FF3300','#9C2B8B','#FF00CC','#FFCC00','#66CCFF','#FFCC66','#99CC00','#CC0066','#000099','#006600','#666600','#0AD3EF','#82DC27','#FDD50C','#FD0CF4','#783255','#11A81A','#E99F19','#19E9AC','#4119E9','#B219E9','#E05B50','#EEEA48', '#A72E71', '#AB5090', '#ABCD34', '#AC4401', '#AD1049', '#B2A139', '#B42DA1', '#B4E0B8', '#B5D2BC', '#B937B7', '#B9D0E6', '#BBF90E', '#BE5415', '#C43C25', '#C6C9BE', '#CAB861', '#CDAAB9', '#D0490F', '#D09F85', '#D34AE9', '#D794D7', '#DC93C1', '#DE3C93', '#E2F8E1', '#E3EE73', '#E52700', '#E5B9DE', '#EC3198', '#EF4DDD', '#EFDE92', '#F04874', '#F0A4E1', '#F31AEC', '#F45CC4', '#F4C928', '#F8FC9E', '#F9DCE9', '#FE466C']

    def __init__ (self,Graph_Data):
        self.graph_data = Graph_Data

    @staticmethod
    def return_sample_type_display_group_colours(sampleTypeDisplayGroups):
        if sampleTypeDisplayGroups is None:
            return []
        newColourArray = get_new_colour_array()

        data = sampleTypeDisplayGroups
        group_members = {}
        return_stepped_colours = {}
        for sample_type in data:
            group = data[sample_type]
            if group not in group_members:
                group_members[group] = 0
            group_members[group] = group_members[group] + 1
        for group in group_members:
            start_colour = newColourArray[group]
            end_colour = '#000000'
            list_of_start_end_colours = [[start_colour,end_colour]]
            number_of_steps = group_members[group]
            return_stepped_colours[group] = Stemformatics_Expression.return_stepped_colours(list_of_start_end_colours,number_of_steps)
        return return_stepped_colours



    def _get_standard_deviation(self,ds_id,chip_id,probe_id):
        r_server = redis.Redis(unix_socket_path=config['redis_server'])
        delimiter = config['redis_delimiter']
                
        row_name = str('standard_deviation'+delimiter+str(ds_id)+delimiter+chip_id+delimiter+probe_id)
        sd_value = r_server.get(row_name)
        #~ raise Error
        if sd_value is None:
            sd_value = 0
            
        return float(sd_value)

    """
        _calculate_grouped_graph_data will go through the probe expression rows from redis 
        which are using probe_id as dictionary and then group this according to the sort_by.
        It will organise and calculate values for scatter/bar/box and line graphs for use 
        when needed later on. This is the place to tweak the way values are aggregated.

        The sort_by is usually Sample Type. This will have two level dictionary
                grouped_graph_data[probe_id][sample_type] 

        If it is not by Sample Type, then this will have a three level dictionary. There are
        two different types of three level dictionaries, one when creating a line graph 
        (LineGraphGroup)and the other for a normal graph with a different sort_by.

        The line graph three level dictionary will look like this:
                grouped_graph_data[probe_id][day][LineGraphGroup]

        The normal three level non-line graph dictionary will look like this:
                grouped_graph_data[probe_id][sort_by][sample_type]


        As you can see, the line graph doesn't use sample type to group at all, while the 
        normal three level dictionary uses sample type. It's a historical purpose where 
        sample type used to be cell type and you weren't allowed to split that up.

        The for loops are for probe_id and then the individual samples (for their 
        expressions). These are all aggregated and values stored in grouped_graph_data.

        After the two foor loops finish, then grouped_graph_data goes into a for loop
        depending on the number of levels in grouped_graph_data. In this loop, statistics
        are calculated via _calculate_statistics such as quartiles, max, min and standard
        deviation for the grouped samples (not to be confused with the standard deviation
        of the technical replicates that are collapsed).  
            

    """ 
    def _calculate_grouped_graph_data(self,groupBy): #CRITICAL-1 - DONE
        if groupBy is None:
            groupBy = 'Sample Type'
            self.sort_by = groupBy
        pylons.app_globals._push_object(config['pylons.app_globals'])

        grouped_graph_data = {}
        count = 0
        metaDataList = {}
        min_value = 0
        for row in self.graph_data.probe_expression_rows:
            
            #row_dict = gene_filtered_matricks_result.todict(row)
            probe_id = row
            sample_count = 0
            grouped_graph_data[probe_id] = {}
            samples_found = []
            for expression_value in self.graph_data.probe_expression_rows[row]:
                if expression_value != '' and expression_value != 'None':
                    expression_value = float(expression_value) 
                    if min_value > expression_value:
                        min_value = expression_value
                else:
                    expression_value = self.lowest_expression_value

                chip_id = self.graph_data.sample_labels[sample_count]
                sample_count += 1
                samples_found.append(chip_id) 
                metaDataValues = g.all_sample_metadata[self.graph_data.chip_type][chip_id][self.graph_data.ds_id]
                sample_id = metaDataValues['Replicate Group ID']
                standard_deviation = self._get_standard_deviation(self.graph_data.ds_id,chip_id,probe_id)
                sampleID = sample_id
                sample_size = 1 # for now
                
                """ 
                This is three levels - for line graph and special group by Disease for example
                Group by Disease will give you a grouped_graph_data[disease_type][sample_type]
                """
                if (groupBy != 'Sample Type' and self.graph_type != 'scatter'):
                    self.data_levels = 3 #probe/first group/second group 
                    if groupBy == 'LineGraphGroup':
                        firstGroupByValue = metaDataValues['Day']
                        secondGroupByValue = metaDataValues[groupBy] #this will be LineGraphGroup
                    else:
                        firstGroupByValue = metaDataValues[groupBy] # eg. groupBy Disease
                        secondGroupByValue = metaDataValues['Sample Type']
                        
                    if firstGroupByValue not in grouped_graph_data[probe_id]:
                        grouped_graph_data[probe_id][firstGroupByValue] = {} 
                        samples_found.append(firstGroupByValue+secondGroupByValue)
                    if secondGroupByValue not in grouped_graph_data[probe_id][firstGroupByValue]:
                        grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue] = {} 
                        samples_found.append(firstGroupByValue+secondGroupByValue)
                    
                        grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['points'] = {} 
                        grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['removed_samples'] = 0 
                        grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['raw_values'] = [] 
                        grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['statistics'] = {} 

                         
                    if expression_value is not None:
                        grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['raw_values'].append(expression_value)
                    else:
                        grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['removed_samples'] += 1
                        
                    grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['points'][sampleID] = {} 
                    grouped_graph_data[probe_id][firstGroupByValue][secondGroupByValue]['points'][sampleID] = {
                                    "expression_value": expression_value,
                                    "standard_deviation": standard_deviation,
                                    "chip_type": self.graph_data.chip_type,
                                    "sample_size": sample_size
                                     }    
                else:
                    self.data_levels = 2 #probe/Sample Type or scatter with disease state
                    groupByValue = metaDataValues[groupBy]
                    if groupByValue not in grouped_graph_data[probe_id]:
                        grouped_graph_data[probe_id][groupByValue] = {}
                        grouped_graph_data[probe_id][groupByValue]['points'] = {}
                        grouped_graph_data[probe_id][groupByValue]['raw_values'] = []
                        grouped_graph_data[probe_id][groupByValue]['removed_samples'] = 0 
                        grouped_graph_data[probe_id][groupByValue]['statistics'] = {}

                    
                    if expression_value is not None:
                        grouped_graph_data[probe_id][groupByValue]['raw_values'].append(expression_value)
                    else:
                        grouped_graph_data[probe_id][groupByValue]['removed_samples'] += 1

                    grouped_graph_data[probe_id][groupByValue]['points'][sampleID] = {}
                    grouped_graph_data[probe_id][groupByValue]['points'][sampleID] = {
                                    "expression_value": expression_value,
                                    "standard_deviation": standard_deviation,
                                    "chip_type": self.graph_data.chip_type,
                                    "sample_size": sample_size
                                     }       
                                          
                count = count + 1


            """
            This is the end of the initial two for loops getting the data ready.
            Now we will go through all the levels and calculate the values for 
            all the graphs like q1,q2, median average etc.
            """
            if self.data_levels == 3:
                for first_group_by_value in grouped_graph_data[probe_id]:
                    for second_first_group_by_value in grouped_graph_data[probe_id][first_group_by_value]:
                        raw_values = grouped_graph_data[probe_id][first_group_by_value][second_first_group_by_value]['raw_values']
                        num_raw_values = len(raw_values)
                        temp_dict = self._calculate_statistics(raw_values) 
                        removed_samples = grouped_graph_data[probe_id][first_group_by_value][second_first_group_by_value]['removed_samples']
                        extra_info = ''
                        if removed_samples != 0:
                            total_samples = removed_samples + num_raw_values
                            extra_info = str(removed_samples)+'/'+str(total_samples)+' samples removed due to floored values' 
                        
                        grouped_graph_data[probe_id][first_group_by_value][second_first_group_by_value]['extra_info']  = extra_info
                        grouped_graph_data[probe_id][first_group_by_value][second_first_group_by_value]['statistics']  = temp_dict

            if self.data_levels == 2:
                for group_by_value in grouped_graph_data[probe_id]:
                    raw_values = grouped_graph_data[probe_id][group_by_value]['raw_values']
                    temp_dict = self._calculate_statistics(raw_values) 
                    num_raw_values = len(raw_values)
                    removed_samples = grouped_graph_data[probe_id][group_by_value]['removed_samples']
                    extra_info = ''
                    if removed_samples != 0:
                        total_samples = removed_samples + num_raw_values
                        extra_info = str(removed_samples)+'/'+str(total_samples)+' samples removed due to floored values' 
                    grouped_graph_data[probe_id][group_by_value]['extra_info']  = extra_info
                    grouped_graph_data[probe_id][group_by_value]['statistics']  = temp_dict

        self.grouped_graph_data = grouped_graph_data
        self.min_value = min_value

    def _calculate_statistics(self,raw_values):
        temp_dict = {}

        if raw_values == []:
            temp_dict['Q1'] = None
            temp_dict['Q3'] = None
            temp_dict['Q2'] = None
            temp_dict['Median'] =None
            temp_dict['Average'] =None
            temp_dict['StandardDeviation'] = None
            temp_dict['Max'] = None
            temp_dict['Min'] = None
            return temp_dict


        temp_dict['Q1'] = percentile(raw_values,0.25)
        temp_dict['Q3'] = percentile(raw_values,0.75)
        temp_dict['Q2'] = percentile(raw_values,0.5)


        temp_dict['Median'] =float(numpy.median(raw_values))
        temp_dict['Average'] =float(numpy.mean(raw_values))
        temp_dict['StandardDeviation'] = float(numpy.std(raw_values))
        temp_dict['Max'] = float(numpy.amax(raw_values))
        temp_dict['Min'] = float(numpy.amin(raw_values))
        return temp_dict

    def return_renamed_probe(self,raw_probe_id):
        position = self.graph_data.raw_probe_list.index(raw_probe_id)
        # if probe_ids shown, then show the gene
        symbol = ""
        if self.graph_data.select_probes is not None:
            try:
                symbol = self.graph_data.probe_dict[raw_probe_id] + ' ' 
            except:
                symbol = '' 
        renamed_probe_id = symbol + self.graph_data.display_probe_list[position]
        return renamed_probe_id


def percentile(N, percent, key=lambda x:x):
    """
    http://stackoverflow.com/questions/2374640/how-do-i-calculate-percentiles-with-python-numpy
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    if not N:
        return None
    N.sort()
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1


# colour array created by http://stackoverflow.com/a/12224359
# returns an array
def get_new_colour_array():
    return ['#CC0066', '#000099', '#006600', '#666600', '#0AD3EF', '#82DC27', '#FDD50C', '#FD0CF4', '#783255', '#11A81A', '#E99F19', '#19E9AC', '#4119E9', '#B219E9', '#E05B50', '#EEEA48', '#A72E71', '#AB5090', '#ABCD34', '#AC4401', '#AD1049', '#B2A139', '#B42DA1', '#B4E0B8', '#B5D2BC', '#B937B7', '#B9D0E6', '#BBF90E', '#BE5415', '#C43C25', '#C6C9BE', '#CAB861', '#CDAAB9', '#D0490F', '#D09F85', '#D34AE9', '#D794D7', '#DC93C1', '#DE3C93', '#E2F8E1', '#E3EE73', '#E52700', '#E5B9DE', '#EC3198', '#EF4DDD', '#EFDE92', '#F04874', '#F0A4E1', '#F31AEC', '#F45CC4', '#F4C928', '#F8FC9E', '#F9DCE9', '#FE466C', '#9BC4E5', '#310106', '#04640D', '#FEFB0A', '#FB5514', '#E115C0', '#00587F', '#0BC582', '#FEB8C8', '#9E8317', '#01190F', '#847D81', '#58018B', '#B70639', '#703B01', '#F7F1DF', '#118B8A', '#4AFEFA', '#FCB164', '#796EE6', '#000D2C', '#53495F', '#F95475', '#61FC03', '#5D9608', '#DE98FD', '#98A088', '#4F584E', '#248AD0', '#5C5300', '#9F6551', '#BCFEC6', '#932C70', '#2B1B04', '#B5AFC4', '#D4C67A', '#AE7AA1', '#C2A393', '#0232FD', '#6A3A35', '#BA6801', '#168E5C', '#16C0D0', '#C62100', '#014347', '#233809', '#42083B', '#82785D', '#023087', '#B7DAD2', '#196956', '#8C41BB', '#ECEDFE', '#2B2D32', '#94C661', '#F8907D', '#895E6B', '#788E95', '#FB6AB8', '#576094', '#DB1474', '#8489AE', '#860E04', '#FBC206', '#6EAB9B', '#F2CDFE', '#645341', '#760035', '#647A41', '#496E76', '#E3F894', '#F9D7CD', '#876128', '#A1A711', '#01FB92', '#FD0F31', '#BE8485', '#C660FB', '#120104', '#D48958', '#05AEE8', '#C3C1BE', '#9F98F8', '#1167D9', '#D19012', '#B7D802', '#826392', '#5E7A6A', '#B29869', '#1D0051', '#8BE7FC', '#76E0C1', '#BACFA7', '#11BA09', '#462C36', '#65407D', '#491803', '#F5D2A8', '#03422C', '#72A46E', '#128EAC', '#47545E', '#B95C69', '#A14D12', '#C4C8FA', '#372A55', '#3F3610', '#D3A2C6', '#719FFA', '#0D841A', '#4C5B32', '#9DB3B7', '#B14F8F', '#747103', '#9F816D', '#D26A5B', '#8B934B', '#F98500', '#002935', '#D7F3FE', '#FCB899', '#1C0720', '#6B5F61', '#F98A9D', '#9B72C2', '#A6919D', '#2C3729', '#D7C70B', '#9F9992', '#EFFBD0', '#FDE2F1', '#923A52', '#5140A7', '#BC14FD', '#6D706C', '#0007C4', '#C6A62F', '#000C14', '#904431', '#600013', '#1C1B08', '#693955', '#5E7C99', '#6C6E82', '#D0AFB3', '#493B36', '#AC93CE', '#C4BA9C', '#09C4B8', '#69A5B8', '#374869', '#F868ED', '#E70850', '#C04841', '#C36333', '#700366', '#8A7A93', '#52351D', '#B503A2', '#D17190', '#A0F086', '#7B41FC', '#0EA64F', '#017499', '#08A882', '#7300CD', '#A9B074', '#4E6301', '#AB7E41', '#547FF4', '#134DAC', '#FDEC87', '#056164', '#FE12A0', '#C264BA', '#939DAD', '#0BCDFA', '#277442', '#1BDE4A', '#826958', '#977678', '#BAFCE8', '#7D8475', '#8CCF95', '#726638', '#FEA8EB', '#EAFEF0', '#6B9279', '#C2FE4B', '#304041', '#1EA6A7', '#022403', '#062A47', '#054B17', '#F4C673', '#02FEC7', '#9DBAA8', '#775551', '#835536', '#565BCC', '#80D7D2', '#7AD607', '#696F54', '#87089A', '#664B19', '#242235', '#7DB00D', '#BFC7D6', '#D5A97E', '#433F31', '#311A18', '#FDB2AB', '#D586C9', '#7A5FB1', '#32544A', '#EFE3AF', '#859D96', '#2B8570', '#8B282D', '#E16A07', '#4B0125', '#021083', '#114558', '#F707F9', '#C78571', '#7FB9BC', '#FC7F4B', '#8D4A92', '#6B3119', '#884F74', '#994E4F', '#9DA9D3', '#867B40', '#CED5C4', '#1CA2FE', '#D9C5B4', '#FEAA00', '#507B01', '#A7D0DB', '#53858D', '#588F4A', '#FBEEEC', '#FC93C1', '#D7CCD4', '#3E4A02', '#C8B1E2', '#7A8B62', '#9A5AE2', '#896C04', '#B1121C', '#402D7D', '#858701', '#D498A6', '#B484EF', '#5C474C', '#067881', '#C0F9FC', '#726075', '#8D3101', '#6C93B2', '#A26B3F', '#AA6582', '#4F4C4F', '#5A563D', '#E83005', '#32492D', '#FC7272', '#B9C457', '#552A5B', '#B50464', '#616E79', '#DCE2E4', '#CF8028', '#0AE2F0', '#4F1E24', '#FD5E46', '#4B694E', '#C5DEFC', '#5DC262', '#022D26', '#7776B8', '#FD9F66', '#B049B8', '#988F73', '#BE385A', '#2B2126', '#54805A', '#141B55', '#67C09B', '#456989', '#DDC1D9', '#166175', '#C1E29C', '#A397B5', '#2E2922', '#ABDBBE', '#B4A6A8', '#A06B07', '#A99949', '#0A0618', '#B14E2E', '#60557D', '#D4A556', '#82A752', '#4A005B', '#3C404F', '#6E6657', '#7E8BD5', '#1275B8', '#D79E92', '#230735', '#661849', '#7A8391', '#FE0F7B', '#B0B6A9', '#629591', '#D05591', '#97B68A', '#97939A', '#035E38', '#53E19E', '#DFD7F9', '#02436C', '#525A72', '#059A0E', '#3E736C', '#AC8E87', '#D10C92', '#B9906E', '#66BDFD', '#C0ABFD', '#0734BC', '#341224', '#8AAAC1', '#0E0B03', '#414522', '#6A2F3E', '#2D9A8A', '#4568FD', '#FDE6D2', '#FEE007', '#9A003C', '#AC8190', '#DCDD58', '#B7903D', '#1F2927', '#9B02E6', '#827A71', '#878B8A', '#8F724F', '#AC4B70', '#37233B', '#385559', '#F347C7', '#9DB4FE', '#D57179', '#DE505A', '#37F7DD', '#503500', '#1C2401', '#DD0323', '#00A4BA', '#955602', '#FA5B94', '#AA766C', '#B8E067', '#6A807E', '#4D2E27', '#73BED7', '#D7BC8A', '#614539', '#526861', '#716D96', '#829A17', '#210109', '#436C2D', '#784955', '#987BAB', '#8F0152', '#0452FA', '#B67757', '#A1659F', '#D4F8D8', '#48416F', '#DEBAAF', '#A5A9AA', '#8C6B83', '#403740', '#70872B', '#D9744D', '#151E2C', '#5C5E5E', '#B47C02', '#F4CBD0', '#E49D7D', '#DD9954', '#B0A18B', '#2B5308', '#EDFD64', '#9D72FC', '#2A3351', '#68496C', '#C94801', '#EED05E', '#826F6D', '#E0D6BB', '#5B6DB4', '#662F98', '#0C97CA', '#C1CA89', '#755A03', '#DFA619', '#CD70A8', '#BBC9C7', '#F6BCE3', '#A16462', '#01D0AA', '#87C6B3', '#E7B2FA', '#D85379', '#643AD5', '#D18AAE', '#13FD5E', '#B3E3FD', '#C977DB', '#C1A7BB', '#9286CB', '#A19B6A', '#8FFED7', '#6B1F17', '#DF503A', '#10DDD7', '#9A8457', '#60672F', '#7D327D', '#DD8782', '#59AC42', '#82FDB8', '#FC8AE7', '#909F6F', '#B691AE', '#B811CD', '#BCB24E', '#CB4BD9', '#2B2304', '#AA9501', '#5D5096', '#403221', '#F9FAB4', '#3990FC', '#70DE7F', '#95857F', '#84A385', '#50996F', '#797B53', '#7B6142', '#81D5FE', '#9CC428', '#0B0438', '#3E2005', '#4B7C91', '#523854', '#005EA9', '#F0C7AD', '#ACB799', '#FAC08E', '#502239', '#BFAB6A', '#2B3C48', '#0EB5D8', '#8A5647', '#49AF74', '#067AE9', '#F19509', '#554628', '#4426A4', '#7352C9', '#3F4287', '#8B655E', '#B480BF', '#9BA74C', '#5F514C', '#CC9BDC', '#BA7942', '#1C4138', '#3C3C3A', '#29B09C', '#02923F', '#701D2B', '#36577C', '#3F00EA', '#3D959E', '#440601', '#8AEFF3', '#6D442A', '#BEB1A8', '#A11C02', '#8383FE', '#A73839', '#DBDE8A', '#0283B3', '#888597', '#32592E', '#F5FDFA', '#01191B', '#AC707A', '#B6BD03', '#027B59', '#7B4F08', '#957737', '#83727D', '#035543', '#6F7E64', '#C39999', '#52847A', '#925AAC', '#77CEDA', '#516369', '#E0D7D0', '#FCDD97', '#555424', '#96E6B6', '#85BB74', '#5E2074', '#BD5E48', '#9BEE53', '#1A351E', '#3148CD', '#71575F', '#69A6D0', '#391A62', '#E79EA0', '#1C0F03', '#1B1636', '#D20C39', '#765396', '#7402FE', '#447F3E', '#CFD0A8', '#3A2600', '#685AFC', '#A4B3C6', '#534302', '#9AA097', '#FD5154', '#9B0085', '#403956', '#80A1A7', '#6E7A9A', '#605E6A', '#86F0E2', '#5A2B01', '#7E3D43', '#ED823B', '#32331B', '#424837', '#40755E', '#524F48', '#B75807', '#B40080', '#5B8CA1', '#FDCFE5', '#CCFEAC', '#755847', '#CAB296', '#C0D6E3', '#2D7100', '#D5E4DE', '#362823', '#69C63C', '#AC3801', '#163132', '#4750A6', '#61B8B2', '#FCC4B5', '#DEBA2E', '#FE0449', '#737930', '#8470AB', '#687D87', '#D7B760', '#6AAB86', '#8398B8', '#B7B6BF', '#92C4A1', '#B6084F', '#853B5E', '#D0BCBA', '#92826D', '#C6DDC6', '#BE5F5A', '#280021', '#435743', '#874514', '#63675A', '#E97963', '#8F9C9E', '#985262', '#909081', '#023508', '#DDADBF', '#D78493', '#363900', '#5B0120', '#603C47', '#C3955D', '#AC61CB', '#FD7BA7', '#716C74', '#8D895B', '#071001', '#82B4F2', '#B6BBD8', '#71887A', '#8B9FE3', '#997158', '#65A6AB', '#2E3067', '#321301', '#FEECCB', '#3B5E72', '#C8FE85', '#A1DCDF', '#CB49A6', '#B1C5E4', '#3E5EB0', '#88AEA7', '#04504C', '#975232', '#6786B9', '#068797', '#9A98C4', '#A1C3C2', '#1C3967', '#DBEA07', '#789658', '#E7E7C6', '#A6C886', '#957F89', '#752E62', '#171518', '#A75648', '#01D26F', '#0F535D', '#047E76', '#C54754', '#5D6E88', '#AB9483', '#803B99', '#FA9C48', '#4A8A22', '#654A5C', '#965F86', '#9D0CBB', '#A0E8A0', '#D3DBFA', '#FD908F', '#AEAB85', '#A13B89', '#F1B350', '#066898', '#948A42', '#C8BEDE', '#19252C', '#7046AA', '#E1EEFC', '#3E6557', '#CD3F26', '#2B1925', '#DDAD94', '#C0B109', '#37DFFE', '#039676', '#907468', '#9E86A5', '#3A1B49', '#BEE5B7', '#C29501', '#9E3645', '#DC580A', '#645631', '#444B4B', '#FD1A63', '#DDE5AE', '#887800', '#36006F', '#3A6260', '#784637', '#FEA0B7', '#A3E0D2', '#6D6316', '#5F7172', '#B99EC7', '#777A7E', '#E0FEFD', '#E16DC5', '#01344B', '#F8F8FC', '#9F9FB5', '#182617', '#FE3D21', '#7D0017', '#822F21', '#EFD9DC', '#6E68C4', '#35473E', '#007523', '#767667', '#A6825D', '#83DC5F', '#227285', '#A95E34', '#526172', '#979730', '#756F6D', '#716259', '#E8B2B5', '#B6C9BB', '#9078DA', '#4F326E', '#B2387B', '#888C6F', '#314B5F', '#E5B678', '#38A3C6', '#586148', '#5C515B', '#CDCCE1', '#C8977F']
