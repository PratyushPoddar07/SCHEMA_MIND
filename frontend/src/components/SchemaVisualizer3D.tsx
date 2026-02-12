import { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame, ThreeEvent } from '@react-three/fiber';
import { Text, OrbitControls, Line } from '@react-three/drei';
import * as THREE from 'three';
import type { SchemaInfo, TableInfo } from '@/types';

interface TableNodeProps {
  table: TableInfo;
  position: [number, number, number];
  onClick: (table: TableInfo) => void;
  isSelected: boolean;
}

function TableNode({ table, position, onClick, isSelected }: TableNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  useFrame((state) => {
    if (meshRef.current && (hovered || isSelected)) {
      meshRef.current.rotation.y = state.clock.elapsedTime;
    }
  });
  
  const handleClick = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    onClick(table);
  };
  
  return (
    <group position={position}>
      <mesh
        ref={meshRef}
        onClick={handleClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial
          color={isSelected ? '#0ea5e9' : hovered ? '#38bdf8' : '#1e293b'}
          emissive={isSelected ? '#0ea5e9' : hovered ? '#38bdf8' : '#000000'}
          emissiveIntensity={isSelected ? 0.5 : hovered ? 0.3 : 0}
          wireframe={!isSelected && !hovered}
        />
      </mesh>
      
      <Text
        position={[0, 2.5, 0]}
        fontSize={0.3}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {table.name}
      </Text>
      
      <Text
        position={[0, -2.5, 0]}
        fontSize={0.2}
        color="#94a3b8"
        anchorX="center"
        anchorY="middle"
      >
        {table.columns.length} columns
      </Text>
    </group>
  );
}

interface RelationshipLineProps {
  start: [number, number, number];
  end: [number, number, number];
}

function RelationshipLine({ start, end }: RelationshipLineProps) {
  const points = useMemo(() => [
    new THREE.Vector3(...start),
    new THREE.Vector3(...end)
  ], [start, end]);
  
  return (
    <Line
      points={points}
      color="#0ea5e9"
      lineWidth={2}
      transparent
      opacity={0.4}
    />
  );
}

interface SchemaVisualizerProps {
  schema: SchemaInfo;
  onTableSelect: (table: TableInfo) => void;
  selectedTable: TableInfo | null;
}

export default function SchemaVisualizer3D({ 
  schema, 
  onTableSelect, 
  selectedTable 
}: SchemaVisualizerProps) {
  const tablePositions = useMemo(() => {
    const tables = Object.values(schema.tables);
    const positions: Record<string, [number, number, number]> = {};
    
    // Arrange tables in a circular layout
    const radius = 8;
    const angleStep = (2 * Math.PI) / tables.length;
    
    tables.forEach((table, index) => {
      const angle = angleStep * index;
      const x = radius * Math.cos(angle);
      const z = radius * Math.sin(angle);
      positions[table.name] = [x, 0, z];
    });
    
    return positions;
  }, [schema]);
  
  const relationships = useMemo(() => {
    return schema.relationships.map((rel) => ({
      start: tablePositions[rel.from_table],
      end: tablePositions[rel.to_table]
    })).filter(rel => rel.start && rel.end);
  }, [schema.relationships, tablePositions]);
  
  return (
    <div className="w-full h-full">
      <Canvas camera={{ position: [0, 15, 15], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        {/* Render relationship lines */}
        {relationships.map((rel, index) => (
          <RelationshipLine
            key={index}
            start={rel.start}
            end={rel.end}
          />
        ))}
        
        {/* Render table nodes */}
        {Object.values(schema.tables).map((table) => (
          <TableNode
            key={table.name}
            table={table}
            position={tablePositions[table.name]}
            onClick={onTableSelect}
            isSelected={selectedTable?.name === table.name}
          />
        ))}
        
        <OrbitControls
          enableZoom={true}
          enablePan={true}
          enableRotate={true}
          minDistance={10}
          maxDistance={30}
        />
        
        <gridHelper args={[40, 40, '#334155', '#1e293b']} />
      </Canvas>
    </div>
  );
}
