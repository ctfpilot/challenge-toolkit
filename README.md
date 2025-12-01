# CTF Pilot's Challenge Toolkit

Challenge Toolkit for CTF Pilot.  
Allows for bootstrapping challenges and pipeline actions on challenges.

## How to run

> [!NOTE]
> We are currently working on making it easier to use the tool.  

The current tool is only provided as the raw python files.  
Therefore, in order to run the tool, first clone this repository:

```sh
git clone https://github.com/ctfpilot/challenge-toolkit
```

In order to install required dependencies, run:

```sh
pip install -r challenge-toolkit/src/requirements.txt
```

> [!IMPORTANT]
> The tool assumes, that the current working directory is the root of a challenge repository.  
> Read more about the expected structure of a challenge repository in the **[Challenge repository structure documentation](#challenge-repository-structure)** section.

You can then run the tool using python:

```sh
python challenge-toolkit/src/ctf.py <command> [options]
```

### Dependencies

Currently, the following dependencies are required:

- Python 3.8 or higher
- `pyyaml` Python package
- `python-slugify` Python package

`pyyaml` and `python-slugify` are defined in the `requirements.txt` file.

### Including it in your project as a git submodule

One way to include it into your own project is to add it as a git submodule:

```sh
git submodule add https://github.com/ctfpilot/challenge-toolkit
```

To then clone your own project with the submodule included, run:

```sh
git clone --recurse-submodules <your-repo-url>
```

Or if you already have cloned your repository, run:

```sh
git submodule update --init --recursive
```

## Commands

The tool provides the following commands:

| Command   | Description                                      |
|-----------|--------------------------------------------------|
| `create`  | Create a new challenge based on the template.    |
| `pipeline`| Run the pipeline actions on all challenges.      |

## Challenge repository structure

> [!IMPORTANT]
> The tool works based on the Challenge repository structure defined below. Working outside a structure like this is not supported.

The tools expect a specific directory structure, where challenges are stored in a `challenges` directory.  
Inside the `challenges` directory, challenges are divided into categories.  
Each challenge is stored in its own directory, named identically to the challenge slug.

Besides the `challenges` directory, there is also a `template` directory, which contains the base templates for kubernetes deployment files.

The structure is as follows:

```txt
.
├── challenges/
│   ├── web
│   ├── forensics
│   ├── rev
│   ├── crypto
│   ├── pwn
│   ├── boot2root
│   ├── osint
│   ├── misc
│   ├── blockchain
│   └── beginner/
│       └── challenge-1
├── template/
├── challenge-toolkit/
└── <other files>
```


### Challenge structure

> [!TIP]
> Challenge source code is located in the `src/` directory.  
> The main files are `challenge.yml`, `description.md` and `README.md`, along with the `src/` directories.

Each challenge is stored in its own directory, named after the challenge slug.
Within the challenge directory, there are several subdirectories and files that make up the challenge.

The subdirectory structure of a challenge is as follows:

```txt
.
├── handout/
├── k8s/
├── solution/
├── src/
├── template/
├── challenge.yml
├── description.md
├── README.md
└── version
```

- `handout/`contains the files that are handed out to the user. This may be the binary that needs to be reversed, the pcap file that needs to be analyzed, etc. The files in this directory are automatically zipped and stored in the `k8s/files/` directory as `<category>_<slug>.zip`.
- `k8s/` contains the kubernetes deployment files for the challenge. This is automatically generated and used for deploying to the CTF platform. This directory should not be modified manually, but instead use the `challenge.yml` file to specify the deployment files.
- `solution/` contains the script that is used to solve the challenge. This is filled out by the challenge creator. No further standard for the content is enforced.
- `src/` contains the source code for the challenge. It contains all the code needed for running the challenge. It may also contain any copies that needs to be handed out. Dockerfiles, python scripts, etc. lives here.
- `template/` contains the template files for the challenge. For example the kubernetes deployment files, or similar, that are rendered with the data from the `challenge.yml` file.
- `challenge.yml` contains the metadata for the challenge. This must be filled out by the challenge creator. Follows a very strict structure, which can be found in the schema file provided in the file.  
  The file may be replaced by a JSON file, as `challenge.json`.
- `description.md` contains the description of the challenge. This is the text that is shown to the user, when they open the challenge. It should be written in markdown.
- `README.md` contains the base idea and informationm of the challenge. May contain inspiration or other internal notes about the challenge. May also contain solution steps.
- `version` contains the version of the challenge. This is automatically updated by the `pipeline` command. Contains a single number, which is the version number of the challenge.

To learn more about the `challenge.yml` file, see the [CTF Pilot's Challenge Schema](https://github.com/ctfpilot/challenge-schema).

### Challenges with Dockerfiles

It is very common to use Docker for challenges, as it is the core for shared and instanced challenges.

Docker images are built using the `pipeline` command.
They are built based on the Dockerfiles provided in the `challenge.yml` file.
Each Dockerfile location is relative to the individual challenge directory.

The following should be described in the `challenge.yml` file for dockerfiles, under the `dockerfile_locations` key:

- `location`: The location of the Dockerfile relative to the challenge directory. Example: `src/Dockerfile`.
- `context`: The context of the Dockerfile relative to the challenge directory. Example: `src/`.  
  Context controls where Docker looks for files to include in the build process.
- `identifier`: The identifier of the Dockerfile to suffix the docker image with. Example: `web`, `db`, `app`, `bot`.
  The identifier is used when multiple Docker images are needed for a challenge.
  *This may be left out, if only a single Dockerfile is described.*

This format follows the [CTF Pilot's Challenge Schema](https://github.com/ctfpilot/challenge-schema).

<details>
    <summary>Click to expand example</summary>
    

An example of multiple Dockerfiles, with one for the app and one for the database:

```yaml
dockerfile_locations:
  - location: src/app/Dockerfile
    context: src/app/
    identifier: app
  - location: src/db/Dockerfile
    context: src/db/
    identifier: db
```

The folder structure for this example would be:

```txt
.
└── src/
    ├── app/
    │   ├── Dockerfile
    │   └── <All other files, for the app>
    └── db/
        ├── Dockerfile
        └── <All other files for the DB>
```

</details>
<br/>

The `pipeline` command tags docker images with the following format:

```txt
ghcr.io/<repo>-<category>-<challenge-slug>-<identifier>:<version|latest>
```

Examples of docker image tags:

With identifier:

```txt
ghcr.io/ctfpilot/example-web-challenge-1-web:latest
```

Without identifier:

```txt
ghcr.io/ctfpilot/example-web-challenge-1:latest
```

## Contributing

We welcome contributions of all kinds, from **code** and **documentation** to **bug reports** and **feedback**!

Please check the [Contribution Guidelines (`CONTRIBUTING.md`)](/CONTRIBUTING.md) for detailed guidelines on how to contribute.

To maintain the ability to distribute contributions across all our licensing models, **all code contributions require signing a Contributor License Agreement (CLA)**.
You can review **[the CLA here](https://github.com/ctfpilot/cla)**. CLA signing happens automatically when you create your first pull request.  
To administrate the CLA signing process, we are using **[CLA assistant lite](https://github.com/marketplace/actions/cla-assistant-lite)**.

*A copy of the CLA document is also included in this repository as [`CLA.md`](CLA.md).*  
*Signatures are stored in the [`cla` repository](https://github.com/ctfpilot/cla).*

## License

This schema and repository is licensed under the **EUPL-1.2 License**.  
You can find the full license in the **[LICENSE](LICENSE)** file.

We encourage all modifications and contributions to be shared back with the community, for example through pull requests to this repository.  
We also encourage all derivative works to be publicly available under the **EUPL-1.2 License**.  
At all times must the license terms be followed.

For information regarding how to contribute, see the [contributing](#contributing) section above.

CTF Pilot is owned and maintained by **[The0Mikkel](https://github.com/The0mikkel)**.  
Required Notice: Copyright Mikkel Albrechtsen (<https://themikkel.dk>)

## Code of Conduct

We expect all contributors to adhere to our [Code of Conduct](/CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive environment for all.
