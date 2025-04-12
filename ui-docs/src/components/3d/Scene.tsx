import React, { useRef, useState, useEffect, useMemo } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import {
  Text,
  Box,
  Sphere,
  Cylinder,
  useGLTF,
  PerspectiveCamera,
  OrbitControls,
  Cloud,
  Environment,
  MeshDistortMaterial,
  MeshWobbleMaterial,
  Sparkles,
  Stars
} from '@react-three/drei';
import * as THREE from 'three';
import { EffectComposer, Bloom, DepthOfField, Vignette } from '@react-three/postprocessing';

interface SceneProps {
  viewMode: 'guided' | 'free' | 'map';
  selectedComponent: string | null;
  onSelectComponent: (name: string) => void;
}

// Custom materials for different component types
const createCustomMaterial = (type: string) => {
  switch (type) {
    case 'Model':
      return (props: any) => (
        <MeshDistortMaterial
          color="#4a00e0"
          emissive="#4a00e0"
          emissiveIntensity={0.4}
          roughness={0.2}
          metalness={0.9}
          distort={0.2}
          speed={2}
          {...props}
        />
      );
    case 'Tool':
      return (props: any) => (
        <MeshWobbleMaterial
          color="#2dcddf"
          emissive="#2dcddf"
          emissiveIntensity={0.3}
          roughness={0.3}
          metalness={0.7}
          factor={0.2}
          speed={1.5}
          {...props}
        />
      );
    case 'Agent':
      return (props: any) => (
        <MeshWobbleMaterial
          color="#00ff9d"
          emissive="#00ff9d"
          emissiveIntensity={0.5}
          roughness={0.1}
          metalness={0.8}
          factor={0.1}
          speed={1}
          {...props}
        />
      );
    default:
      return (props: any) => (
        <MeshDistortMaterial
          color={componentColors[type as keyof typeof componentColors] || new THREE.Color('#ffffff')}
          emissive={componentColors[type as keyof typeof componentColors] || new THREE.Color('#ffffff')}
          emissiveIntensity={0.2}
          roughness={0.4}
          metalness={0.6}
          distort={0.1}
          speed={1}
          {...props}
        />
      );
  }
};

// Particle System Component for connections
const ParticleFlow: React.FC<{
  start: [number, number, number];
  end: [number, number, number];
  color: string;
  count?: number;
  size?: number;
  speed?: number;
}> = ({ start, end, color, count = 20, size = 0.05, speed = 0.5 }) => {
  const particlesRef = useRef<THREE.Points>(null);

  // Create points along the path
  const { positions, colors } = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const color3 = new THREE.Color(color);

    for (let i = 0; i < count; i++) {
      // Random position along the line
      const t = Math.random();
      positions[i * 3] = start[0] + (end[0] - start[0]) * t;
      positions[i * 3 + 1] = start[1] + (end[1] - start[1]) * t;
      positions[i * 3 + 2] = start[2] + (end[2] - start[2]) * t;

      // Color with slightly random variation
      colors[i * 3] = color3.r * (0.9 + Math.random() * 0.2);
      colors[i * 3 + 1] = color3.g * (0.9 + Math.random() * 0.2);
      colors[i * 3 + 2] = color3.b * (0.9 + Math.random() * 0.2);
    }

    return { positions, colors };
  }, [start, end, color, count]);

  // Animate particles along the path
  useFrame(() => {
    if (particlesRef.current) {
      const positions = particlesRef.current.geometry.attributes.position.array as Float32Array;

      for (let i = 0; i < count; i++) {
        // Move along the line
        const x = positions[i * 3];
        const y = positions[i * 3 + 1];
        const z = positions[i * 3 + 2];

        const dx = end[0] - start[0];
        const dy = end[1] - start[1];
        const dz = end[2] - start[2];

        positions[i * 3] += dx * speed * 0.01;
        positions[i * 3 + 1] += dy * speed * 0.01;
        positions[i * 3 + 2] += dz * speed * 0.01;

        // If particle has reached the end, reset to start with some randomness
        const distToEnd = Math.sqrt(
          Math.pow(positions[i * 3] - end[0], 2) +
          Math.pow(positions[i * 3 + 1] - end[1], 2) +
          Math.pow(positions[i * 3 + 2] - end[2], 2)
        );

        if (distToEnd < 0.3) {
          positions[i * 3] = start[0] + (Math.random() - 0.5) * 0.2;
          positions[i * 3 + 1] = start[1] + (Math.random() - 0.5) * 0.2;
          positions[i * 3 + 2] = start[2] + (Math.random() - 0.5) * 0.2;
        }
      }

      particlesRef.current.geometry.attributes.position.needsUpdate = true;
    }
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={count}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={size}
        vertexColors
        transparent
        opacity={0.8}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
};

// Animation paths for guided tour with enhanced positions for better viewing
const guidedPositions = {
  'start': new THREE.Vector3(0, 2, 15),
  'Model': new THREE.Vector3(-5, 1, 8),
  'Tool': new THREE.Vector3(0, 1, 7),
  'Agent': new THREE.Vector3(5, 1, 8),
  'Llama3': new THREE.Vector3(-7, -2, 9),
  'Qwen2.5-7B': new THREE.Vector3(-4, -2, 8),
  'Other Models': new THREE.Vector3(-1, -2, 7),
};

// Enhanced colors with more vivid tones for different components
const componentColors = {
  'Model': new THREE.Color('#6215ff'),
  'Tool': new THREE.Color('#15e6ff'),
  'Agent': new THREE.Color('#00ffa3'),
  'Llama3': new THREE.Color('#9370FF'),
  'Qwen2.5-7B': new THREE.Color('#7842FF'),
  'Other Models': new THREE.Color('#5e35b1'),
};

const ComponentNode: React.FC<{
  position: [number, number, number];
  name: string;
  selected: boolean;
  onClick: () => void;
  color: THREE.Color;
  scale?: number;
}> = ({ position, name, selected, onClick, color, scale = 1 }) => {
  const nodeRef = useRef<THREE.Mesh>(null);
  const textRef = useRef<THREE.Object3D>(null);
  const [hovered, setHovered] = useState(false);
  const CustomMaterial = createCustomMaterial(name);

  // Calculate animation values based on component type and state
  const rotationSpeed = name === 'Model' ? 0.003 : name === 'Tool' ? 0.004 : 0.002;
  const pulseSpeed = selected ? 2 : hovered ? 1.5 : 1;
  const hoverScale = selected ? 1.3 : hovered ? 1.2 : 1;

  // Use a more dynamic animation pattern
  useFrame((state) => {
    if (nodeRef.current) {
      // Complex rotation patterns based on component type
      nodeRef.current.rotation.y += rotationSpeed;

      if (name === 'Model') {
        nodeRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
      } else if (name === 'Tool') {
        nodeRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 0.4) * 0.1;
      } else if (name === 'Agent') {
        nodeRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.2) * 0.05;
        nodeRef.current.rotation.z = Math.cos(state.clock.elapsedTime * 0.3) * 0.05;
      }

      // Smoother scale transitions
      nodeRef.current.scale.x = THREE.MathUtils.lerp(nodeRef.current.scale.x, scale * hoverScale, 0.1);
      nodeRef.current.scale.y = THREE.MathUtils.lerp(nodeRef.current.scale.y, scale * hoverScale, 0.1);
      nodeRef.current.scale.z = THREE.MathUtils.lerp(nodeRef.current.scale.z, scale * hoverScale, 0.1);

      // Subtle breathing effect
      const breathingFactor = 1 + Math.sin(state.clock.elapsedTime * pulseSpeed) * 0.03;
      nodeRef.current.scale.multiplyScalar(breathingFactor);
    }

    if (textRef.current) {
      // Position text above the node and make it face the camera
      textRef.current.position.y = nodeRef.current ? nodeRef.current.position.y + 1.5 : position[1] + 1.5;
      textRef.current.quaternion.copy(state.camera.quaternion);

      // Text scale animation when selected
      const textScale = selected || hovered ? 1.2 : 1;
      textRef.current.scale.setScalar(textScale);
    }
  });

  // Different shapes for different component types
  const getGeometry = () => {
    if (name === 'Model') {
      return <dodecahedronGeometry args={[0.7, 1]} />; // Complex crystalline structure
    } else if (name === 'Tool') {
      return <octahedronGeometry args={[0.7, 0]} />; // Tool-like shape
    } else if (name === 'Agent') {
      return <icosahedronGeometry args={[0.7, 0]} />; // More complex for agents
    } else {
      return <torusKnotGeometry args={[0.5, 0.2, 64, 8, 2, 3]} />; // Special for subtypes
    }
  };

  return (
    <>
      <mesh
        ref={nodeRef}
        position={position}
        onClick={onClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        {getGeometry()}
        <CustomMaterial
          emissiveIntensity={selected ? 0.8 : hovered ? 0.6 : 0.3}
        />
      </mesh>

      {/* Particles around selected/hovered components */}
      {(selected || hovered) && (
        <Sparkles
          count={20}
          scale={[3, 3, 3]}
          size={0.4}
          speed={0.3}
          color={color}
          position={position}
        />
      )}

      {/* Enhanced text with glow effect */}
      <Text
        ref={textRef}
        position={[position[0], position[1] + 1.5, position[2]]}
        color={selected || hovered ? "#ffffff" : "#ccccff"}
        fontSize={0.5}
        maxWidth={2}
        textAlign="center"
        anchorX="center"
        anchorY="middle"
        font="/fonts/Inter-Bold.woff"
        outlineWidth={0.02}
        outlineColor={color.getHex()}
      >
        {name}
      </Text>
    </>
  );
};

const Connection: React.FC<{
  start: [number, number, number];
  end: [number, number, number];
  color: string;
  active: boolean;
}> = ({ start, end, color, active }) => {
  const midPoint = [
    (start[0] + end[0]) / 2,
    (start[1] + end[1]) / 2,
    (start[2] + end[2]) / 2,
  ];

  // Calculate vector and length between points
  const vec = new THREE.Vector3(
    end[0] - start[0],
    end[1] - start[1],
    end[2] - start[2]
  );
  const length = vec.length();

  // Create a rotation quaternion from the (0,1,0) vector to our direction vector
  const cylinderDirection = new THREE.Vector3(0, 1, 0);
  const direction = vec.clone().normalize();
  const quaternion = new THREE.Quaternion().setFromUnitVectors(
    cylinderDirection,
    direction
  );

  // Use a glowing, animated material for the connection
  const [glowIntensity, setGlowIntensity] = useState(0.2);

  useFrame((state) => {
    if (active) {
      // Pulsing glow effect when active
      const pulse = 0.3 + Math.sin(state.clock.elapsedTime * 4) * 0.2;
      setGlowIntensity(pulse);
    } else {
      // Subtle ambient glow when inactive
      const ambient = 0.2 + Math.sin(state.clock.elapsedTime * 1.5) * 0.05;
      setGlowIntensity(ambient);
    }
  });

  return (
    <>
      {/* Base connection line */}
      <Cylinder
        args={[0.03, 0.03, length, 8]}
        position={midPoint as [number, number, number]}
        rotation={[0, 0, 0]}
        quaternion={quaternion}
      >
        <meshStandardMaterial
          color={color}
          transparent={true}
          opacity={0.4}
          emissive={color}
          emissiveIntensity={glowIntensity}
        />
      </Cylinder>

      {/* Particle flow along connection */}
      <ParticleFlow
        start={start}
        end={end}
        color={color}
        count={active ? 30 : 15}
        speed={active ? 2 : 0.5}
        size={active ? 0.08 : 0.05}
      />
    </>
  );
};

const Scene: React.FC<SceneProps> = ({ viewMode, selectedComponent, onSelectComponent }) => {
  const sceneRef = useRef<THREE.Group>(null);
  const [currentTourStop, setCurrentTourStop] = useState<string>('start');
  const { camera } = useThree();

  // Enhanced component positions with more depth and structure
  const positions = {
    'Model': [-4, 0, 0] as [number, number, number],
    'Tool': [0, 0, 0] as [number, number, number],
    'Agent': [4, 0, 0] as [number, number, number],
    'Llama3': [-6, -3, 1] as [number, number, number],
    'Qwen2.5-7B': [-4, -3, 1] as [number, number, number],
    'Other Models': [-2, -3, 1] as [number, number, number],
  };

  // Enhanced connections between components with active state tracking
  const connections = [
    { from: 'Model', to: 'Agent', color: '#7028e4' },
    { from: 'Tool', to: 'Agent', color: '#2dcddf' },
    { from: 'Llama3', to: 'Model', color: '#4a00e0' },
    { from: 'Qwen2.5-7B', to: 'Model', color: '#4a00e0' },
    { from: 'Other Models', to: 'Model', color: '#4a00e0' },
  ];

  // Determine active connections based on selected component
  const isConnectionActive = (from: string, to: string) => {
    return selectedComponent === from || selectedComponent === to;
  };

  // Handle camera animation for the guided tour
  useEffect(() => {
    if (viewMode === 'guided') {
      const tourStops = Object.keys(guidedPositions);
      const currentIndex = tourStops.indexOf(currentTourStop);
      const nextStop = tourStops[(currentIndex + 1) % tourStops.length];

      const timer = setTimeout(() => {
        setCurrentTourStop(nextStop);
        if (nextStop !== 'start') {
          onSelectComponent(nextStop);
        } else {
          onSelectComponent('');
        }
      }, 5000); // Change view every 5 seconds

      return () => clearTimeout(timer);
    }
  }, [viewMode, currentTourStop, onSelectComponent]);

  // Animate camera position based on view mode and selected component
  useFrame((state) => {
    if (viewMode === 'guided') {
      // Smooth camera transition during guided tour
      const targetPosition = guidedPositions[currentTourStop];

      state.camera.position.x = THREE.MathUtils.lerp(
        state.camera.position.x,
        targetPosition.x,
        0.05
      );
      state.camera.position.y = THREE.MathUtils.lerp(
        state.camera.position.y,
        targetPosition.y,
        0.05
      );
      state.camera.position.z = THREE.MathUtils.lerp(
        state.camera.position.z,
        targetPosition.z,
        0.05
      );

      // Look at center point
      state.camera.lookAt(0, 0, 0);
    } else if (viewMode === 'map') {
      // Top-down view for map mode
      state.camera.position.x = THREE.MathUtils.lerp(state.camera.position.x, 0, 0.05);
      state.camera.position.y = THREE.MathUtils.lerp(state.camera.position.y, 15, 0.05);
      state.camera.position.z = THREE.MathUtils.lerp(state.camera.position.z, 0, 0.05);
      state.camera.lookAt(0, 0, 0);
    } else if (selectedComponent && viewMode === 'free') {
      // In free mode, gently focus on selected component without fully controlling camera
      const position = positions[selectedComponent as keyof typeof positions];
      if (position) {
        const targetX = position[0];
        const targetY = position[1];
        const targetZ = position[2] + 5; // Stay a bit back from the component

        // Subtle guidance rather than forced movement
        state.camera.position.x = THREE.MathUtils.lerp(
          state.camera.position.x,
          targetX * 0.3 + state.camera.position.x * 0.7,
          0.02
        );
        state.camera.position.y = THREE.MathUtils.lerp(
          state.camera.position.y,
          targetY * 0.3 + state.camera.position.y * 0.7,
          0.02
        );
      }
    }
  });

  return (
    <>
      {/* Post-processing effects for enhanced visuals */}
      <EffectComposer>
        <Bloom luminanceThreshold={0.2} luminanceSmoothing={0.9} height={300} />
        <DepthOfField focusDistance={0} focalLength={0.02} bokehScale={2} height={480} />
        <Vignette eskil={false} offset={0.1} darkness={0.5} />
      </EffectComposer>

      <group ref={sceneRef}>
        {/* Ambient light */}
        <ambientLight intensity={0.2} />

        {/* Main directional light */}
        <directionalLight position={[5, 5, 5]} intensity={0.8} />

        {/* Accent lights for dramatic effect */}
        <pointLight position={[-10, 5, 5]} intensity={0.5} color="#6215ff" />
        <pointLight position={[10, -5, 5]} intensity={0.5} color="#00ffa3" />

        {/* Background elements */}
        <Stars radius={100} depth={50} count={1000} factor={4} saturation={0.5} />
        <Cloud position={[0, 5, -15]} speed={0.2} opacity={0.1} />

        {/* Environment map for reflections */}
        <Environment preset="night" />

        {/* Main components */}
        {Object.entries(positions).map(([name, position]) => (
          <ComponentNode
            key={name}
            position={position}
            name={name}
            selected={selectedComponent === name}
            onClick={() => onSelectComponent(name)}
            color={componentColors[name as keyof typeof componentColors] || new THREE.Color('#ffffff')}
            scale={name === 'Model' || name === 'Tool' || name === 'Agent' ? 1 : 0.7}
          />
        ))}

        {/* Connections between components */}
        {connections.map((conn, idx) => (
          <Connection
            key={idx}
            start={positions[conn.from as keyof typeof positions]}
            end={positions[conn.to as keyof typeof positions]}
            color={conn.color}
            active={isConnectionActive(conn.from, conn.to)}
          />
        ))}

        {/* Background sphere */}
        <Sphere args={[50, 32, 32]} position={[0, 0, -25]}>
          <meshBasicMaterial color="#050914" side={THREE.BackSide} />
        </Sphere>
      </group>
    </>
  );
};

export default Scene;
