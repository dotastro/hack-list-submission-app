from github import InputGitTreeElement


def add_files(repo, branch, message, files):
    """
    Add a new file to a new branch in a GitHub repo
    """

    # Get commit then git commit (not sure about the difference)
    commit = repo.get_branch('master').commit
    git_commit = repo.get_git_commit(commit.sha)

    # We need to include all the files in the master branch
    tree_input = []
    for element in repo.get_git_tree(commit.sha).tree:
        tree_input.append(InputGitTreeElement(element.path,
                                              element.mode,
                                              element.type,
                                              sha=element.sha))

    # We now make a blob with the new file contents and add it to the tree
    for filename, content in files.items():
        content, encoding = content
        blob = repo.create_git_blob(content=content, encoding=encoding)
        tree_input.append(InputGitTreeElement(filename, "100644", "blob", sha=blob.sha))

    # We make a new tree, commit, and branch
    tree = repo.create_git_tree(tree=tree_input)
    commit = repo.create_git_commit(tree=tree, message=message, parents=[git_commit])
    ref = repo.create_git_ref(ref="refs/heads/{0}".format(branch), sha=commit.sha)
    return ref, commit


YML_TEMPLATE = """
title: {title}
creators: {creators}
description: {desc}
source-url: {src}
live-url: {live}
contact-email: {email}
doi: {doi}
images: {images}
orcid: {orcid}
"""
def make_file_contents(request, image_filename):

    title = request.form['title']
    desc = request.form['description']
    src = request.form['source_url']
    live = request.form['live_url']
    doi = request.form['doi']
    email = request.form['email']
    images = image_filename

    creators = [s.strip() for s in request.form['creators'].split(',')]
    creators = '\n    - ' + '\n    - '.join(creators)

    orcid = [s.strip() for s in request.form['orcid'].split(',')]
    orcid = '\n    - ' + '\n    - '.join(orcid)

    return YML_TEMPLATE.format(**locals())
