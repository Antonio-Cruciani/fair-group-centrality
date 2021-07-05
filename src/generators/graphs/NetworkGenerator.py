import os
import src.generators.graphs.BarabasiAlbert as ba
import src.generators.graphs.ErdosRenyi as er
import src.generators.graphs.SBM as sbm


def create_directory_if_not_exists(dir_path):
    if not os.path.isdir(dir_path):
        try:
            os.mkdir(dir_path)
        except OSError:
            raise IOError('Cannot create directory', dir_path)


def generate_network(network_type,
                     n,
                     p=None,
                     q=None,
                     k=None,
                     communities_structure="bfs",
                     number_of_communities=None,
                     communities_size=None,
                     threshold=3):

    save_path = os.getcwd() + '/datasets/synthetic/'

    # Check the type of graph
    if network_type == 'BA':
        # Create the folder for the type of graph
        save_path += 'barabasi_albert/'
        create_directory_if_not_exists(save_path)

        # Create the folder for the size of the network
        save_path += 'n' + str(n) + '/'
        create_directory_if_not_exists(save_path)

        # Check that the value k (number of attachments per node) was provided
        if k is None:
            raise ValueError('A Barabasi-Albert graph requires the parameter k')

        # Create the folder for k
        save_path += 'k' + str(k) + '/'
        create_directory_if_not_exists(save_path)

        _generate_network_with_community_structure(save_path, network_type, n, p, q, k, communities_structure,
                                                   number_of_communities, communities_size, threshold)

    elif network_type == 'ER':
        # Create the folder for the type of graph
        save_path += 'erdos_renyi/'
        create_directory_if_not_exists(save_path)

        # Create the folder for the size of the network
        save_path += 'n' + str(n) + '/'
        create_directory_if_not_exists(save_path)

        # Check that the value p (probability of attachment) was provided
        if p is None:
            raise ValueError('An Erdos-Renyi graph requires the parameter p')

        # Create the folder for p
        save_path += 'p' + str(p) + '/'
        create_directory_if_not_exists(save_path)

        _generate_network_with_community_structure(save_path, network_type, n, p, q, k, communities_structure,
                                                   number_of_communities, communities_size, threshold)

    elif network_type == "SBM":
        # Create the folder for the type of graph
        save_path += 'sbm/'
        create_directory_if_not_exists(save_path)

        # Create the folder for the size of the network
        save_path += 'n' + str(n) + '/'
        create_directory_if_not_exists(save_path)

        # Check that the value p (probability of in-attachment) was provided
        if p is None:
            raise ValueError('A SBM graph requires the parameter p')

        # Create the folder for p
        save_path += 'p' + str(p) + '/'
        create_directory_if_not_exists(save_path)

        # Check that the value q (probability of out-attachment) was provided
        if q is None:
            raise ValueError('A SBM graph requires the parameter q')

        # Create the folder for q
        save_path += 'q' + str(q) + '/'
        create_directory_if_not_exists(save_path)

        _generate_network_with_community_structure(save_path, network_type, n, p, q, k, communities_structure,
                                                   number_of_communities, communities_size, threshold)

    else:
        raise ValueError('network_type have to be one of the following values: BA, ER or SBM')


def _generate_network_with_community_structure(dir_path,
                                               network_type,
                                               n,
                                               p=None,
                                               q=None,
                                               k=None,
                                               communities_structure="bfs",
                                               number_of_communities=None,
                                               communities_size=None,
                                               threshold=3):
    save_path = dir_path

    if communities_structure == 'bfs':
        # Create the folder for the community structure of the graph
        save_path += 'cs_bfs/'
        create_directory_if_not_exists(save_path)

        # Check that the threshold for the bfs community generation method was provided
        if threshold is None:
            raise ValueError('the BFS community structure requires a threshold')

        # Create the folder for the threshold
        save_path += 'c_threshold' + str(threshold) + '/'
        create_directory_if_not_exists(save_path)

        # Check the type of graph and save the graph
        if network_type == 'BA':
            ba_graph = ba.BarabasiAlbert(n=n, k=k,communities_structure=communities_structure,communities_size= [],treshold=threshold)
            ba_graph.run()
            print(save_path)
            ba_graph.save_graph(save_path)

        elif network_type == 'ER':
            er_graph = er.ErdosRenyi(n=n, p=p, communities_structure=communities_structure, communities_size= [],treshold=threshold)
            er_graph.run()
            er_graph.save_graph(save_path)

        elif network_type == "SBM":
            raise ValueError('bfs community structure cannot be used with SBM network generation method')
            # sbm_graph = sbm.SBM(n=n, p=p, q=q, number_of_communities=number_of_communities)

    elif communities_structure == 'rd':
        # Create the folder for the community structure of the graph
        save_path += 'cs_rd/'
        create_directory_if_not_exists(save_path)

        # Check that the community number was provided
        if number_of_communities is None:
            raise ValueError('the Random community structure requires the number of communities as parameter')

        # Create the folder for the threshold
        save_path += 'c' + str(number_of_communities) + '/'
        create_directory_if_not_exists(save_path)

        # Check the type of graph and save the graph
        if network_type == 'BA':
            ba_graph = ba.BarabasiAlbert(n=n, k=k, communities_number=number_of_communities,
                                         communities_structure=communities_structure)
            ba_graph.save_graph(save_path)

        elif network_type == 'ER':
            er_graph = er.ErdosRenyi(n=n, p=p, communities_number=number_of_communities,
                                     communities_structure=communities_structure)
            er_graph.save_graph(save_path)

        elif network_type == "SBM":
            sbm_graph = sbm.SBM(n=n, p=p, q=q, number_of_communities=number_of_communities)
            sbm_graph.save_graph(save_path)

    elif communities_structure == 'man':
        # Create the folder for the community structure of the graph
        save_path += 'cs_manual/'
        create_directory_if_not_exists(save_path)

        # Check that the community number was provided
        if number_of_communities is None:
            raise ValueError('the Manual community structure requires the number of communities as parameter')

        # Create the folder for the threshold
        save_path += 'c' + str(number_of_communities) + '/'
        create_directory_if_not_exists(save_path)

        # Check the type of graph and save the graph
        if network_type == 'BA':
            ba_graph = ba.BarabasiAlbert(n=n, k=k, communities_number=number_of_communities,
                                         communities_structure=communities_structure, communities_size=communities_size)
            ba_graph.save_graph(save_path)

        elif network_type == 'ER':
            er_graph = er.ErdosRenyi(n=n, p=p, communities_number=number_of_communities,
                                     communities_structure=communities_structure, communities_size=communities_size)
            er_graph.save_graph(save_path)

        elif network_type == "SBM":
            sbm_graph = sbm.SBM(n=n, p=p, q=q, number_of_communities=number_of_communities)
            sbm_graph.save_graph(save_path)

    elif communities_structure == 'auto':
        # Create the folder for the community structure of the graph
        save_path += 'cs_automatic/'
        create_directory_if_not_exists(save_path)

        # Check the type of graph and save the graph
        if network_type == 'BA':
            ba_graph = ba.BarabasiAlbert(n=n, k=k, communities_structure=communities_structure)
            ba_graph.save_graph(save_path)

        elif network_type == 'ER':
            er_graph = er.ErdosRenyi(n=n, p=p, communities_structure=communities_structure)
            er_graph.save_graph(save_path)

        elif network_type == "SBM":
            raise ValueError('Automatic community detection cannot be used with SBM')
            # sbm_graph = sbm.SBM(n=n, p=p, q=q, number_of_communities=number_of_communities)
            # sbm_graph.save_graph(save_path)

    else:
        raise ValueError("The value for communities_structure have to be one of the following: bfs, rd, man, auto")
