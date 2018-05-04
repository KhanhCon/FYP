import FYPArangodb, MyGithub, FYPComposer

def fetchJob(db,project):
    print(project)
    commits = MyGithub.get_commits(project['github_fullname'], since=project["latest_commit"])
    if len(commits) == 0:
        return
    for commit in commits:
        library = {'github_fullname': project['github_fullname'],
                   '_id': project['_id']}
        FYPArangodb.insertJob(db, library, commit["sha"], commit['commit']['author']['date'], status="pending")

def fetchJobs(db):
    aql_projects = "FOR lib IN libraries FILTER lib.type == 'project' RETURN lib"
    projects = db.AQLQuery(aql_projects, rawResults=True, batchSize=750)
    print(len(projects))
    for project in projects:
        fetchJob(db, project)

def fetchDependencies(db, project, SHA_number, commit_date):
    DependenciesPackages = FYPComposer.getDependenciesPackages(project['github_fullname'], SHA_number)
    if DependenciesPackages == None:
        return
    revision = FYPArangodb.insert_revision(db, sha=SHA_number, commitDate=commit_date)['doc']
    version = FYPArangodb.link_version(db, project["_id"], revision['_id'])['doc']

    for package in DependenciesPackages:
        dependency = FYPArangodb.insert_lib(db, package)['doc']
        use = FYPArangodb.link_use(db, revision['_id'], dependency['_id'])['doc']

def executeJob(db, job):
    fetchDependencies(db, project=job["library"], SHA_number=job["_key"], commit_date=job['date'])
    aql_job_set_done = "UPDATE document(@jobID) WITH {status:'done'} IN jobs"
    db.AQLQuery(aql_job_set_done, bindVars={'jobID': job["_id"]}, batchSize=1, rawResults=True)

def fetchGraph(db):
    aql_jobs_pending = "for job in jobs filter job.status == 'pending' return job"
    jobs_pending = db.AQLQuery(aql_jobs_pending, batchSize=20000, rawResults=True)
    print len(jobs_pending)
    for job in jobs_pending:
        print(job)
        executeJob(db, job)


if __name__ == "__main__":
    from pyArango.connection import *
    conn = Connection(username="root", password="root")
    db = conn["TEST"]
    fetchJobs(db)
    fetchGraph(db)

    # 'jobs/c8499db3fd515af4018d655f0cb1c72c8fa07eec'
    #
    # job = db.AQLQuery('return document("jobs/6f914dfc217e8f0f245e65f3d0cf973202a094e5")', rawResults=True )[0]
    # print executeJob(db, job)

    # doc = db.AQLQuery('return document("libraries/16042002")', rawResults=True )
    # print(doc[0]['github_fullname'])
    # dep = fetchDependencies(db, doc[0], '6f914dfc217e8f0f245e65f3d0cf973202a094e5', 'sssss')
