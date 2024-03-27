import os
import pydot
import graphviz


def create_dot_graph(repo, dir_path, branch_name):

    # Get the merged branch you want to visualize
    branch = repo.remote().refs[branch_name]

    # Create a directed graph
    graph = pydot.Dot(graph_type='digraph')

    # Traverse through the commits of the branch
    for commit in repo.iter_commits(branch):
        # Add each commit as a node in the graph
        node = pydot.Node(commit.hexsha, label=commit.message.splitlines()[0])
        graph.add_node(node)

        # Connect the commit to its parent(s)
        for parent in commit.parents:
            edge = pydot.Edge(parent.hexsha, commit.hexsha)
            graph.add_edge(edge)

    # Output the graph to a .dot file
    output_file = os.path.join(dir_path, f'{branch_name}_graph.dot')
    graph.write(output_file)

    convert_to_image(output_file)


def convert_to_image(dot_file_path):
    # Load the DOT file
    with open(dot_file_path, 'r') as file:
        dot_content = file.read()

    # Create a Graphviz graph object
    graph = graphviz.Source(dot_content)

    # Render the graph to an image file
    graph.render(dot_file_path, format='png')
    print(dot_file_path)
