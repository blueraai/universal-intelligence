import React, { useRef, useState, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Box, Sphere, Cylinder } from '@react-three/drei';
import * as THREE from 'three';

interface SceneProps {
  viewMode: 'guided' | 'free' | 'map';
  selectedComponent: string | null;
  onSelectComponent: (name: string) => void;
}

// Animation paths for guided tour
const guidedPositions = {
  'start': new THREE.Vector3(0, 0, 10),
  'Model': new THREE.Vector3(-3, 0, 5),
  'Tool': new THREE.Vector3(0, 0, 5),
  'Agent': new THREE.Vector3(3, 0, 5),
  'Llama3': new THREE.Vector3(-5, -3, 6),
  'Qwen2.5-7B': new THREE.Vector3(-3, -3, 6),
  'Other Models': new THREE.Vector3(-1, -3, 6),
};

// Colors for different components
const componentColors = {
  'Model': new THREE.Color('#4a00e0'),
  'Tool': new THREE.Color('#2dcddf'),
  'Agent': new THREE.Color('#00ff9d'),
  'Llama3': new THREE.Color('#4a00e0').multiplyScalar(0.8),
  'Qwen2.5-7B': new THREE.Color('#4a00e0').multiplyScalar(0.8),
  'Other Models': new THREE.Color('#4a00e0').multiplyScalar(0.8),
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

  useFrame(() => {
    if (nodeRef.current) {
      nodeRef.current.rotation.y += 0.005;

      if (selected || hovered) {
        nodeRef.current.scale.x = THREE.MathUtils.lerp(nodeRef.current.scale.x, scale * 1.2, 0.1);
        nodeRef.current.scale.y = THREE.MathUtils.lerp(nodeRef.current.scale.y, scale * 1.2, 0.1);
        nodeRef.current.scale.z = THREE.MathUtils.lerp(nodeRef.current.scale.z, scale * 1.2, 0.1);
      } else {
        nodeRef.current.scale.x = THREE.MathUtils.lerp(nodeRef.current.scale.x, scale, 0.1);
        nodeRef.current.scale.y = THREE.MathUtils.lerp(nodeRef.current.scale.y, scale, 0.1);
        nodeRef.current.scale.z = THREE.MathUtils.lerp(nodeRef.current.scale.z, scale, 0.1);
      }
    }

    if (textRef.current) {
      textRef.current.position.y = nodeRef.current ? nodeRef.current.position.y + 1.5 : position[1] + 1.5;
      textRef.current.quaternion.copy(new THREE.Quaternion()); // Face the camera
    }
  });

  return (
    <>
      <Box
        ref={nodeRef}
        args={[1, 1, 1]}
        position={position}
        onClick={onClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={selected || hovered ? 0.5 : 0.2}
          roughness={0.4}
          metalness={0.8}
        />
      </Box>
      <Text
        ref={textRef}
        position={[position[0], position[1] + 1, position[2]]}
        color="white"
        fontSize={0.5}
        maxWidth={2}
        textAlign="center"
        anchorX="center"
        anchorY="middle"
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
}> = ({ start, end, color }) => {
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

  return (
    <Cylinder
      args={[0.05, 0.05, length, 8]}
      position={midPoint as [number, number, number]}
      rotation={[0, 0, 0]}
      quaternion={quaternion}
    >
      <meshStandardMaterial
        color={color}
        transparent={true}
        opacity={0.7}
        emissive={color}
        emissiveIntensity={0.2}
      />
    </Cylinder>
  );
};

const Scene: React.FC<SceneProps> = ({ viewMode, selectedComponent, onSelectComponent }) => {
  const sceneRef = useRef<THREE.Group>(null);
  const [currentTourStop, setCurrentTourStop] = useState<string>('start');

  // Define component positions
  const positions = {
    'Model': [-3, 0, 0] as [number, number, number],
    'Tool': [0, 0, 0] as [number, number, number],
    'Agent': [3, 0, 0] as [number, number, number],
    'Llama3': [-5, -3, 0] as [number, number, number],
    'Qwen2.5-7B': [-3, -3, 0] as [number, number, number],
    'Other Models': [-1, -3, 0] as [number, number, number],
  };

  // Define connections between components
  const connections = [
    { from: 'Model', to: 'Agent', color: '#7028e4' },
    { from: 'Tool', to: 'Agent', color: '#2dcddf' },
    { from: 'Llama3', to: 'Model', color: '#4a00e0' },
    { from: 'Qwen2.5-7B', to: 'Model', color: '#4a00e0' },
    { from: 'Other Models', to: 'Model', color: '#4a00e0' },
  ];

  // Handle guided tour
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

  return (
    <group ref={sceneRef}>
      {/* Ambient light */}
      <ambientLight intensity={0.2} />

      {/* Directional light */}
      <directionalLight position={[5, 5, 5]} intensity={0.8} />

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
        />
      ))}

      {/* Background sphere */}
      <Sphere args={[30, 32, 32]} position={[0, 0, -15]}>
        <meshBasicMaterial color="#050914" side={THREE.BackSide} />
      </Sphere>
    </group>
  );
};

export default Scene;
