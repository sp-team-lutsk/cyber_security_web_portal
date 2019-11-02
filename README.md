# Title "Cyber security web portal"

> Web portal for students and teachers of Cybersecurity department of Lutsk National Technical University

## Table of Contents

- [Last Updates](#last-updates)
- [Installation](#installation)
- [Features](#features)
- [Contributing](#contributing)
- [Team](#team)
- [FAQ](#faq)
- [Support](#support)
- [License](#license)

---

## Last Updates

- 18.07.19 Django version changed to 2.2.3
- 19.07.19 Mongodb integrated
- 05.07.19 Added models 
- 14.08.19 Added tests for models
- 19.08.19 Added serializers
- 25.09.19 Added frontend part with nginx
- 20.10.19 Added backend part with news parsing
- 20.10.19 Added some fixes to server part
- 23.10.19 Swagger API Docs added to project
- 23.10.19 Updated Pillow to 6.2.0 (Security alert)
- 25.10.19 Restructured authentication API, urls changed
- 26.10.19 'Student' page added to front-end
- 27.10.18 Permissions models created

## Installation

Make this simple steps to run this project. :smile: 😄

### Clone

- Clone this repo to your local machine using `https://github.com/sp-team-lutsk/docker_polls_group.git`

### Setup

- Install all dependencies from file `dev.txt` via command :point_down::

> Using Python 3

```shell
$ pip install -r api/requirements/dev.txt
```
> Using Docker scripts
```
- docker_all-in.sh - you can run this script when you start project first time. It will clean your docker, init new container, make migrations and create admin user
- docker_clean_all.sh - deletes old containers
- docker_init.sg - inits new docker-container
- docker_update_db.sh - updates migrations
- docker_api_create_su.sh - creates superuser
- docker_start.sh - starts docker-container
- docker-nosetests.sh - runs tests 
```
---

## Features
It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).

## Documentation
Now you can find API docs in the same name dir in project's root

## Tests

- You can run tests with docker script `docker-nosetests.sh`

---

## Contributing

> To get started...

### Step 1

- **Option 1**
    - 👯 Clone this repo to your local machine using `https://github.com/sp-team-lutsk/cyber_security_web_portal.git

- **Option 2**
    - Create your own branch using `git checkout -b name_of_your_branch`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull request using <a href="https://github.com/sp-team-lutsk/cyber_security_web_portal/compare" target="_blank">`https://github.com/sp-team-lutsk/cyber_security_web_portal/compare`</a>.

---

## Team (table)

> Or Contributors/People

| Name                                                       | Role      |
| ---------------------------------------------------------- | ---------:|
| <a href="https://github.com/Martinfree">Martinfree</a>     | Back-end  |
| <a href="https://github.com/romaoksenyuk">romaoksenyuk</a> | Back-end  |
| <a href="https://github.com/Green5tar">Green5tar</a>       | Parsing   |
| <a href="https://github.com/joni2881">joni2881</a>         | Front-end |
| <a href="https://github.com/vitalities">vitalities</a>     | Front-end |
| <a href="https://github.com/Pavel1179">Pavel1179</a>       | Front-end |
| <a href="https://github.com/Azrael-git">Azrael</a>         | PM        |
| <a href="https://github.com/m-pasha">m-pasha</a>           | CEO       |
| <a href="https://github.com/klekhaav">klekhaav</a>         | Boss      | 

---

## FAQ

- **How do I do *specifically* so and so?**
    - No problem! Just do this.

---

## Support

Reach out to me at one of the following places!

- Website that will help you <a href="http://google.com" target="_blank">`google.com`</a>

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2019 © <a href="#" target="_blank">Our Team</a>.
