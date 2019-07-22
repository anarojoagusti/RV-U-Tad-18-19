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
#include <memory>
#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
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
	//glEnable(GL_BLEND);
	//glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS);
	return true;
}

int main() {

	// Init GLFW para generar la ventana
	if (glfwInit() != GLFW_TRUE) {
		std::cout << "could not initalize glfw" << std::endl;
		return false;
	}
	atexit(glfwTerminate);

	// Creo la ventana
    GLFWwindow *window = glfwCreateWindow(800, 600, "Ana Rojo Window", FULLSCREEN ? glfwGetPrimaryMonitor() : nullptr, nullptr);
    if (!window) {
        std::cout << "could not create glfw window" << std::endl;
        return -10;
    }
    glfwMakeContextCurrent(window);

	//Compruebo que el motor ha sido inicializado
	if (!init()) {
		return -11;
	}
	if (!window) {
		return -12;
	}

	//Generación del shader por defecto 
	std::string vertexShader = readString("../data/vertex.shd");
	std::string fragmentShader = readString("../data/fragment.shd");
	Shader shader(vertexShader, fragmentShader);
	shader.use();

	State::defaultShader = std::make_shared<Shader>(shader);

	// Creo la cámara
	int screenWidth, screenHeight;
	glfwGetWindowSize(window, &screenWidth, &screenHeight);

	std::shared_ptr<Camera> mainCamera = std::make_shared<Camera>();
	mainCamera->setClearColor(glm::vec3(0.2f, 0.6f, 1.0f));
	mainCamera->setPosition(glm::vec3(0.0f, 1.0f, 0.0f));
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

		glm::ivec4 halfVP = mainCamera->getViewport() / 2;
		glm::vec2 viewportCenter = { halfVP.z, halfVP.w };

		double xpos = 0, ypos = 0;
		glfwGetCursorPos(window, &xpos, &ypos);
		glm::vec2 currMousePos(xpos, ypos);
		currMousePos = (viewportCenter - currMousePos) / viewportCenter;

		glm::quat xQuad = glm::rotate(glm::quat(), currMousePos.x, glm::vec3(0.0f, 1.0f, 0.0f));
		glm::quat yQuad = glm::rotate(glm::quat(), currMousePos.y, glm::vec3(1.0f, 0.0f, 0.0f));
		mainCamera->setRotation(xQuad * yQuad);
	});

	// Creo el mundo
	std::shared_ptr<World> world = std::make_shared<World>();
	world->addEntity(mainCamera);

	//// Cargo la malla Asian Town
	std::shared_ptr<Mesh> meshAsia = Mesh::load("../data/asian_town.msh.xml");
	std::shared_ptr<Model> modelAsia = std::make_shared<Model>(meshAsia);
	modelAsia->setScale(glm::vec3(10.0f, 10.0f, 10.0f));
	world->addEntity(modelAsia);

	//// Luz Puntual  y luz ambiente
	world->setAmbient(glm::vec3(1.0f, 1.0f, 1.0f));
	std::shared_ptr<Light> pLight = std::make_shared<Light>(Light::Type::POINT, glm::vec3(0, 0, 0));
	pLight->setColor(glm::vec3(0.5, 0.5, 0.5));
	pLight->setLinearAttenuation(0.2);
	world->addEntity(pLight);

	float lastTime = static_cast<float>(glfwGetTime());
	while (!glfwWindowShouldClose(window) && !glfwGetKey(window, GLFW_KEY_ESCAPE)) {
		// update delta time
		float newTime = static_cast<float>(glfwGetTime());
		float deltaTime = newTime - lastTime;
		lastTime = newTime;

		int screenWidth, screenHeight;
		glfwGetWindowSize(window, &screenWidth, &screenHeight);
		mainCamera->setProjection(glm::perspective(glm::pi<float>() / 3.0f, screenWidth / static_cast<float>(screenHeight), 0.001f, 100.0f));
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
