# SOARCA Fin Library
A Python implementation for the SOARCA FIN, compatible with: SOARCA the TNO orchestrator for Open-C2, CACAO and STIX
For more information about the SOARCA, we refer the reader to the [website](https://cossas.github.io/SOARCA/) of the SOARCA project.
For more in depth documentation, see the documentation page on here.

## Quick Use
To use the SOARCA Fin library use the following command to install the library using pip:
```bash
pip install soarca-fin-library
```

## Example
```python
def capability_pong_callback(command: Command) -> ResultStructure:
    print("Received ping, returning pong!")

    result = Variable(
        type=VariableTypeEnum.string,
        name="pong_output",
        description="If ping, return pong",
        value="pong",
        constant=True,
        external=False)

    context = command.command.context

    return ResultStructure(
        state="success", context=context, variables={"result": result})


def main(mqtt_broker: str, mqtt_port: int, username: str, password: str) -> None:

    finId = "soarca-fin--pingpong-f877bb3a-bb37-429e-8ece-2d4286cf326d"
    agentName = "soarca-fin-pong-f896bb3b-bb37-429e-8ece-2d4286cf326d"
    externalReferenceName = "external-reference-example-name"
    capabilityId = "mod-pong--e896aa3b-bb37-429e-8ece-2d4286cf326d"

    # Create AgentStructure
    agent = AgentStructure(
        name=agentName)

    # Create ExternalReference
    external_reference = ExternalReference(name=externalReferenceName)

    # Create StepStructure
    step_structure = StepStructure(
        name="step_name",
        description="step description",
        external_references=[external_reference],
        command="pong",
        target=agentName)

    # Create CapabilityStructure
    capability_structure = CapabilityStructure(
        capability_id=capabilityId,
        type=WorkFlowStepEnum.action,
        name="Ping Pong capability",
        version="0.0.1",
        step={
            "test": step_structure},
        agent={
            "testagent": agent})

    # Create Soarca fin
    fin = SoarcaFin(finId)
    # Set config for MQTT Server
    fin.set_config_MQTT_server(mqtt_broker, mqtt_port, username, password)
    # Register Capabilities
    fin.create_fin_capability(capability_structure, capability_pong_callback)
    # Start the fin
    fin.start_fin()


if __name__ == "__main__":
    load_dotenv()
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    USERNAME = os.getenv("MQTT_USERNAME", "soarca")
    PASSWD = os.getenv("MQTT_PASSWD", "password")

    main(MQTT_BROKER, MQTT_PORT, USERNAME, PASSWD)
```

## Setup SOARCA Capabilities
To register a fin to SOARCA, first create a `SoarcaFin` object and pass the `fin_id` in the constructor.
Call `set_config_MQTT_server()` to set the required configurations for the fin to connect to the MQTT broker.
For each capability to be registered, call `create_fin_capability()`. The capability callback funtion should return an object of type `ResultStructure`.
When all capabilities are initialized, call `start_fin()` for the SOARCA Fin to connect to the MQTT broker and register itself to SOARCA.

An example is given in this project in the file `examples/pong_example.py`


## Contributing
Want to contribute to this project? Please keep in mind the following rules:
- This repository uses git **rebase** strategy
- For each PR, there should be atleasts one issue
- Make sure all tests pass (including lint errors)


### Running this repository
#### Requirements
 - Python3
 - Poetry

#### Setup
##### Env File
In order to run the project, create an `.env` file in the root of the project with the following entries:
```bash
MQTT_BROKER = "{INSERT_MQTT_BROKER_URL_HERE}"
MQTT_PORT = "{INSERT_MQTT_PORT_HERE}"
MQTT_USERNAME = "{INSERT_USERNAME_HERE}"
MQTT_PASSWD = "{INSERT_PASSWORD_HERE}"
```
If no `.env` file is specified, the following default values will be used:
```bash
MQTT_BROKER = "localhost"
MQTT_PORT = "1883"
MQTT_USERNAME = "soarca"
MQTT_PASSWD = "password"
```

##### Dependencies
To handle dependencies in this project, the package Poetry is used.
To install Poetry execute the following command:
```bash
pip3 install poetry
```

To install the dependencies from the `pyproject.toml` either enter a poetry shell, create a virtual environment or use poetry run.
To enter a poetry shell execute the following command in the root of the project:
```bash
poetry shell
```

To install the dependencies in a poetry shell or create a virtual environment, run:
```bash
poetry install
```

### Quick Run
To quick run the project, either run it through poetry run or a poetry shell.
#### Poetry Run
```bash
poetry run python examples/pong_example.py
```

#### Poetry Shell
```bash
python examples/pong_example.py
```

### Running tests
To run the tests in this repository use:
```bash
poetry run python -m unittest
``` 
To run python linter, first install pylint and then run pylint with the following arguments:
```bash
poetry add pylint &&
poetry run pylint --disable=R,C $(git ls-files '*.py')
```
To format the code base, first install ruff and then run ruff:
```bash
poetry add ruff &&
poetry run ruff format
```
