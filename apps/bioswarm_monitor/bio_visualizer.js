/**
 * BioSwarm: AlphaFold-Style 3D Visualizer
 * Uses Three.js to render protein structures as 'Cartoon' ribbons.
 */

let scene, camera, renderer, line;
let chainGroup;

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0xffffff, 0.8);
    pointLight.position.set(50, 50, 100);
    scene.add(pointLight);

    camera.position.z = 100;

    // Chain Container
    chainGroup = new THREE.Group();
    scene.add(chainGroup);

    // Ghost Line
    const geometry = new THREE.BufferGeometry();
    const material = new THREE.LineBasicMaterial({ color: 0x00f2ff, opacity: 0.1, transparent: true });
    line = new THREE.Line(geometry, material);
    scene.add(line);

    animate();
    fetchData();
}

async function fetchData() {
    try {
        const response = await fetch('bio_snapshot.json?t=' + Date.now());
        if (!response.ok) throw new Error("Snapshot not found");
        const data = await response.json();
        updateVisualization(data.residues, data.ss);
        document.getElementById('status').innerText = "LIVE: FOLDING...";
    } catch (e) {
        document.getElementById('status').innerText = "WAITING FOR ENGINE...";
    }
    setTimeout(fetchData, 100);
}

function updateVisualization(positions, ss) {
    if (!positions || positions.length === 0) return;
    if (!chainGroup) return;

    const countEl = document.getElementById('residue-count');
    if (countEl) countEl.innerText = positions.length + " Residues";

    chainGroup.clear();

    const points = positions.map(p => new THREE.Vector3(p[0], p[1], p[2]));
    const bbox = new THREE.Box3();
    points.forEach(p => bbox.expandByPoint(p));

    // Rainbow Gradient Color Map
    const getColor = (i) => {
        const hue = i / positions.length;
        return new THREE.Color().setHSL(0.6 - hue * 0.6, 1.0, 0.5);
    };

    // Segmented Cartoon Rendering
    for (let i = 0; i < points.length - 1; i++) {
        const type = ss ? ss[i] : 'C';
        const p1 = points[i];
        const p2 = points[i+1];
        
        let geometry, thickness;
        if (type === 'H') { // Alpha Helix: Thicker Tube
            thickness = 1.0;
            geometry = new THREE.TubeGeometry(new THREE.LineCurve3(p1, p2), 4, thickness, 8, false);
        } else if (type === 'S') { // Beta Sheet: Flat Box/Arrow
            thickness = 0.4;
            const curve = new THREE.LineCurve3(p1, p2);
            geometry = new THREE.BoxGeometry(2.0, thickness, p1.distanceTo(p2));
            const mesh = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color: 0xffcc00, metalness: 0.5, roughness: 0.2 }));
            mesh.position.copy(p1.clone().add(p2).multiplyScalar(0.5));
            mesh.lookAt(p2);
            chainGroup.add(mesh);
            continue;
        } else { // Coil: Thin Tube
            thickness = 0.2;
            geometry = new THREE.TubeGeometry(new THREE.LineCurve3(p1, p2), 4, thickness, 8, false);
        }

        const material = new THREE.MeshStandardMaterial({ 
            color: getColor(i),
            metalness: 0.7,
            roughness: 0.2
        });
        const mesh = new THREE.Mesh(geometry, material);
        chainGroup.add(mesh);
    }

    // Auto-scale camera
    const size = bbox.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const targetZ = maxDim * 2.5 + 40;
    camera.position.z += (targetZ - camera.position.z) * 0.05;
}

function animate() {
    requestAnimationFrame(animate);
    if (scene) scene.rotation.y += 0.005;
    if (renderer && scene && camera) renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
});

// Start initialization
init();
