# Multi Host Deployment

Multi Host Deployment refer to the way of deploying a stack of docker container 
on multiple hosts, working together as if it is one cluster of machines communicate
with each other. Docker already support this natively using `docker stack` command
which will deploy the orchestration described by docker-compose file to a system
of clustered machines called `docker swarm`. This allows us to easily scale containers,
duplicate it into several containers which works the same way. To allow these 
containers to work with each other, an architecture (of the whole service) 
is needed to describe how these containers relate with each other. This 
architecture can be described by docker-compose file. But, to allow a multi hosts 
architecture, we have to use docker-compose version 3. There is also a lot of 
things to consider when aiming a multi host deployment, such as how to store 
all of the data.

Storing data in multi host architecture requires many containers, possibly in 
different host to be able to access the same set of data. With this requirements 
two options can be considered, first is using a shared storage, second is using 
a replicated storage. By the time this article is written, replication option 
was not really mature. It was hard to replicate storage to be used by different 
containers at the same time, but it was ok to use a replication system to make 
backups or a fallback mechanism, in case the main storage fails. The first option
requires a big shared storage that can be accessed using network (like via CIFS).
This shared storage can also be composed of smaller storage which is managed by 
GlusterFS, for example. All of this container will refer to the same shared storage.

By using docker-compose version 3 for multi host deployment, it is not feasible
to build the docker image when we deploy the services. We have to prepare a 
separate infrastructure to build the images from source code then store it to 
docker-hub. By storing it on docker hub, we have a ready to use container with 
versioning schemes. This will allow us to just download the container when doing 
multi host deployment. This infrastructure needs to be automatic with minimal 
human interaction. By updating the code, it should trigger docker build and upload 
the image automatically for the latest working branch. In addition, we should 
also have a separate versioned images built weekly or monthly.

# Infrastructure

The infrastructure for supporting multi hosts deployment can consists of several 
services:

- Shared Storage Services
- Backup Services
- Docker Image Builder Services
- Deployment Services

## Shared Storage Services

Shared storage services can consists of several storage tied together. The main 
idea is using this storage services as mount point for several folders and databases.

Requirements:

- Big storage
- Ability to mount over network (CIFS, etc)
- BtSync (for replication)

## Backup Services

Backup Services is basically another storage which is replicated from shared storage 
services with some frequency for periodic backup, and also some recent backup as 
failover if the shared storage service is down.

Requirements:

- Big storage
- Ability to mount over network (CIFS, etc)
- BtSync (for replication)


## Docker Image Builder Services

This services builds necessary docker image from related source code. The implementation 
can be a regular server with cronjobs to build and push images daily. It can also 
be a continous integration service, which can build the image and test it at the 
same time.

Requirements:

- Docker engine (for building and pushing images)
- Optionally CI installed is better (like Teamcity). If we decided to use teamcity
  We might need another two server for teamcity worker/agents.
- Cronjob to build images daily, or git webhook


## Deployment Services

This services is used to manage containers and deploy the service stack together. 
We can use either docker swarm or rancher. The requirements is pretty much the same.

Rancher requirements:

- One server for rancher server container. Will be used to manage deployment. 
  Should have an open web port
- Several rancher agent to run the actual containers of the stack. We can also 
  give tag/label to indicate which agent is most suitable for a certain containers,
  like high performance celery worker, etc.


# Summary Diagram

![Summary Diagram](img/Multi%20Hosts%20Deployment/Infrastructures.png?raw=True)
