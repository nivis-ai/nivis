var renderer;
var scene;
var camera;
var composer;
var object, circle, skelet, particle;

window.onload = function() {
    init();
    animate();
}

function init() {
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.autoClear = false;
    renderer.setClearColor(0x000000, 0);
    document.getElementById('canvas').appendChild(renderer.domElement);

    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x000000, 1, 1000);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.z = 400;
    scene.add(camera);

    object = new THREE.Object3D();
    circle = new THREE.Object3D();
    skelet = new THREE.Object3D();
    particle = new THREE.Object3D();

    scene.add(object);
    scene.add(circle);
    scene.add(skelet);
    scene.add(particle);

    var geometry = new THREE.TetrahedronGeometry(2, 0);
    var geometry7 = new THREE.TetrahedronGeometry(2, 2);
    var geom = new THREE.IcosahedronGeometry(7, 1);
    var geom2 = new THREE.IcosahedronGeometry(15, 1);

    var material = new THREE.MeshPhongMaterial({
        color: 0x353535,
        shading: THREE.FlatShading
    });
    var material7 = new THREE.MeshPhongMaterial({
        color: 0x111111,
        shading: THREE.FlatShading
    });

    for (var i = 0; i < 50; i++) {
        var mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize();
        mesh.position.multiplyScalar(200 + Math.random() * 400);
        mesh.rotation.set(Math.random() * 2, Math.random() * 2, Math.random() * 2);
        mesh.scale.x = mesh.scale.y = mesh.scale.z = 15;
        object.add(mesh);
    }

    for (var i = 0; i < 1000; i++) {
        var mesh = new THREE.Mesh(geometry7, material7);
        mesh.position.set(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize();
        mesh.position.multiplyScalar(90 + (Math.random() * 700));
        mesh.rotation.set(Math.random() * 2, Math.random() * 2, Math.random() * 2);
        particle.add(mesh);
    }

    var mat = new THREE.MeshPhongMaterial({
        color: 0xffffff,
        shading: THREE.FlatShading
    });

    var mat2 = new THREE.MeshPhongMaterial({
        color: 0x555555,
        wireframe: true,
        side: THREE.DoubleSide
    });

    var planet = new THREE.Mesh(geom, mat);
    planet.scale.x = planet.scale.y = planet.scale.z = 12;
    circle.add(planet);

    var planet2 = new THREE.Mesh(geom2, mat2);
    planet2.scale.x = planet2.scale.y = planet2.scale.z = 8;
    skelet.add(planet2);

    var ambientLight = new THREE.AmbientLight(0x353535);
    scene.add(ambientLight);

    var directionalLight = new THREE.DirectionalLight(0xffffff);
    directionalLight.position.set(1, 1, 1).normalize();
    scene.add(directionalLight);

    window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);

    object.rotation.x += 0.0030;
    object.rotation.y += 0.0030;
    particle.rotation.x += 0.0000;
    particle.rotation.y -= 0.0040;
    circle.rotation.x -= 0.0020;
    circle.rotation.y -= 0.0020;
    skelet.rotation.x -= 0.0010;
    skelet.rotation.y += 0.0010;
    renderer.clear();

    renderer.render(scene, camera);
}
