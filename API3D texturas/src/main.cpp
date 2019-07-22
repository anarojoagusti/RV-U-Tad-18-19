#define STB_IMAGE_IMPLEMENTATION

#include "../lib/glew/glew.h"
#include "../lib/glfw3/glfw3.h"
#include "Buffer.h"
#include "Shader.h"
#include "Vertex.h"
#include "State.h"
#include "World.h"
#include "Mesh.h"
#include "Model.h"
#include "Camera.h"
#include "Material.h"
#include "Entity.h"
#include "Light.h"
#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include <array>
#include <fstream>
#include <iostream>
#include <sstream>

//Lectura de archivos
std::string readString(const char *filename) {
    std::ifstream f(filename, std::ios_base::binary);
    std::stringstream ss;
    ss << f.rdbuf();
    return ss.str();
}

#define FULLSCREEN false

//Inicializacion del motor
bool init() {
    // Init GLEW
    if (glewInit() != 0) {
        std::cout << "could not initialize glew" << std::endl;
        return false;
    }

    //Habilito OpenGL States
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_SCISSOR_TEST);
	glEnable(GL_BLEND);
	glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS);

	//Generación del shader por defecto 
	std::string vertexShader = readString("../data/vertex.shd");
	std::string fragmentShader = readString("../data/fragment.shd");
	Shader shader(vertexShader, fragmentShader);
    shader.use();

	State::defaultShader = std::make_shared<Shader>(shader);

	return true;
}

int main() {

	// Init GLFW para generar la ventana
	if (glfwInit() != GLFW_TRUE) {
		std::cout << "could not initalize glfw" << std::endl;
		return false;
	}

	// Creo la ventana
    GLFWwindow *window = glfwCreateWindow(800, 600, "Ana Rojo Window", FULLSCREEN ? glfwGetPrimaryMonitor() : nullptr, nullptr);
    if (window == nullptr) {
        std::cout << "could not create glfw window" << std::endl;
        return -15;
    }
    glfwMakeContextCurrent(window);

	//Compruebo que el motor ha sido inicializado
	if (!init()) {
		return -10;
	}

    atexit(glfwTerminate);

	// Creo el mundo
	std::shared_ptr<World> world = std::make_shared<World>();

	// Creo la cámara
	std::shared_ptr<Camera> mainCamera = std::make_shared<Camera>();
	mainCamera->setClearColor(glm::vec3(0.0f, 0.0f, 0.0f));
	mainCamera->setPosition(glm::vec3(0.0f, 5.0f, 0.0f));
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
 
	mainCamera->setUpdate([mainCamera, window](float dt) {
        if (glfwGetKey(window, GLFW_KEY_W)) {
            mainCamera->move(glm::vec3(0.0f, 0.0f, -1.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_A)) {
            mainCamera->move(glm::vec3(-1.0f, 0.0f, 0.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_S)) {
            mainCamera->move(glm::vec3(0.0f, 0.0f, 1.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_D)) {
            mainCamera->move(glm::vec3(1.0f, 0.0f, 0.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_SPACE)) {
            mainCamera->move(glm::vec3(0.0f, 1.0f, 0.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_LEFT_CONTROL) || glfwGetKey(window, GLFW_KEY_RIGHT_CONTROL)) {
            mainCamera->move(glm::vec3(0.0f, -1.0f, 0.0f)*dt);
        }

        glm::ivec4 halfVP = mainCamera->getViewport()/2;
        glm::vec2 viewportCenter = { halfVP.z, halfVP.w };


        double xpos = 0, ypos = 0;
        glfwGetCursorPos(window, &xpos, &ypos);
        glm::vec2 currMousePos(xpos, ypos);
        currMousePos = (viewportCenter - currMousePos) / viewportCenter;
        
        glm::quat xQuad = glm::rotate(glm::quat(), currMousePos.x, glm::vec3(0.0f, 1.0f, 0.0f));
        glm::quat yQuad = glm::rotate(glm::quat(), currMousePos.y, glm::vec3(1.0f, 0.0f, 0.0f));
        mainCamera->setRotation(xQuad * yQuad);
	});
	world->addEntity(mainCamera);

	// Skybox
	std::shared_ptr<Mesh> meshSkybox = Mesh::load("../data/skybox.msh.xml");
	std::shared_ptr<Model> modelSkybox = std::make_shared<Model>(meshSkybox);
	modelSkybox->setScale(glm::vec3(10.0f, 10.0f, 10.0f));
	world->addEntity(modelSkybox);

	// Cube1
	std::shared_ptr<Mesh> meshCube1 = Mesh::load("../data/cube.msh.xml");
	std::shared_ptr<Model> modelCube1 = std::make_shared<Model>(meshCube1);
	modelCube1->setScale(glm::vec3(0.4f, 0.4f, 0.4f));
	modelCube1->setPosition(glm::vec3(0.0f, -0.5f, -1.0f));
	world->addEntity(modelCube1);

	//Cube2
	std::shared_ptr<Mesh> meshCube2 = Mesh::load("../data/teapot_reflect.msh.xml");
	std::shared_ptr<Model> modelCube2 = std::make_shared<Model>(meshCube2);
	modelCube2->setScale(glm::vec3(0.4f, 0.4f, 0.4f));
	modelCube2->setPosition(glm::vec3(0.0f, -0.5f, 1.0f));
	world->addEntity(modelCube2);

	//Cube3
	std::shared_ptr<Mesh> meshCube3 = Mesh::load("../data/suzanne_refract.msh.xml");
	std::shared_ptr<Model> modelCube3 = std::make_shared<Model>(meshCube3);
	modelCube3->setScale(glm::vec3(0.4f, 0.4f, 0.4f));
	modelCube3->setPosition(glm::vec3(1.0f, -0.5f, 0.0f));
	world->addEntity(modelCube3);

	//// Lights and ambient
	world->setAmbient(glm::vec3(1.0f, 1.0f, 1.0f));

	std::shared_ptr<Light> pLight = std::make_shared<Light>(Light::Type::POINT, glm::vec3(0, 0, 0));
	pLight->setColor(glm::vec3(0.5, 0.5, 0.5));
	pLight->setLinearAttenuation(0.2);
	world->addEntity(pLight);

	//Movimiento del cursor
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
	double lastMX, lastMY;
	glfwGetCursorPos(window, &lastMX, &lastMY);

	auto lastTime = static_cast<float>(glfwGetTime());
	float accumulatedTime = 0.0f;
	while (glfwWindowShouldClose(window) == 0 && glfwGetKey(window, GLFW_KEY_ESCAPE) == 0) {
		// Update delta time
		auto newTime = static_cast<float>(glfwGetTime());
		float deltaTime = newTime - lastTime;
		lastTime = newTime;
		accumulatedTime += deltaTime;

		// Get updated screen size
		int screenWidth, screenHeight;
		glfwGetWindowSize(window, &screenWidth, &screenHeight);

		int frameBufferWidth, frameBufferHeight;
		glfwGetFramebufferSize(window, &frameBufferWidth, &frameBufferHeight);

		double mouseX, mouseY;
		glfwGetCursorPos(window, &mouseX, &mouseY);
		float speedMX = static_cast<int>(mouseX - lastMX);
		float speedMY = static_cast<int>(mouseY - lastMY);
		lastMX = mouseX;
		lastMY = mouseY;

		int up = glfwGetKey(window, GLFW_KEY_W);
		int left = glfwGetKey(window, GLFW_KEY_A);
		int down = glfwGetKey(window, GLFW_KEY_S);
		int right = glfwGetKey(window, GLFW_KEY_D);
		glm::vec3 pos = mainCamera->getPosition();

		for (int i = 0; i < world->getNumEntities(); ++i) {
			std::shared_ptr<Camera> isCamera = std::dynamic_pointer_cast<Camera>(world->getEntity(i));

			if (!isCamera) {}
			else {

				mainCamera->setRotation(glm::vec3(mainCamera->getRotation().x - speedMY, mainCamera->getRotation().y - speedMX, 0));

				if (up == GLFW_PRESS) {
					mainCamera->move(glm::vec3(0, 0, -deltaTime * 2));
				}
				if (down == GLFW_PRESS) {
					mainCamera->move(glm::vec3(0, 0, deltaTime * 2));
				}
				if (left == GLFW_PRESS) {
					mainCamera->move(glm::vec3(-deltaTime * 2, 0, 0));
				}
				if (right == GLFW_PRESS) {
					mainCamera->move(glm::vec3(deltaTime * 2, 0, 0));
				}
			}
		}

		mainCamera->setPosition(glm::vec3(0.0f, 1.0f, 2.0f));
		mainCamera->setRotation(glm::vec3(-5, accumulatedTime * 5, 0));
		mainCamera->move(glm::vec3(0.0f, 0.0f, 1.0f));

		modelSkybox->setPosition(mainCamera->getPosition());
		pLight->setPosition(mainCamera->getPosition() + glm::vec3(0.0f, 0.0f, -0.0001f));

		mainCamera->setProjection(glm::perspective(glm::radians(90.0f), static_cast<float>(screenWidth) / static_cast<float>(screenHeight), 0.1f, 100.0f));
		mainCamera->setViewport(glm::ivec4(0, 0, screenWidth, screenHeight));
		//Preparo segun la posicion de la cámara, actualizo los valores State
		mainCamera->prepare();
		//Pinto en la ventana
		world->update(deltaTime);
		world->draw();

        // Swapeo buffers y actualizo eventos
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    return 0;
}
