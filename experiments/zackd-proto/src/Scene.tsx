// Lights + camera rig + actors. Lighting per VISUAL_GRAMMAR 5: big soft key from above/front, world-blue fill
// (hemisphere), warm gold rim from behind the subject (re-aimed per shot), warm practical through the door.
import React, {useState} from 'react';
import {useThree} from '@react-three/fiber';
import {Object3D, PerspectiveCamera} from 'three';
import {Breath, FrostMotes, HeatAura} from './fx';
import {Character, PovArm, charPose, povArmAt} from './Character';
import {Set} from './Set';
import {auraVisible, cameraAt, heat, outsideLight, roomLight} from './timeline';

const CameraRig: React.FC<{t: number}> = ({t}) => {
	const camera = useThree((s) => s.camera) as PerspectiveCamera;
	const c = cameraAt(t);
	camera.position.set(...c.pos);
	camera.fov = c.fov;
	camera.near = 0.02;
	camera.far = 40;
	camera.lookAt(...c.target);
	camera.updateProjectionMatrix();
	return null;
};

export const Scene: React.FC<{t: number}> = ({t}) => {
	const cam = cameraAt(t);
	const shot = cam.shot;
	const pose = charPose(t);
	const room = roomLight(t);
	const out = outsideLight(t);
	// rim light sits behind the subject relative to the camera
	const subj = shot.showChar ? [pose.pos[0], 1.2, pose.pos[2]] : cam.target;
	const dx = subj[0] - cam.pos[0];
	const dz = subj[2] - cam.pos[2];
	const dl = Math.hypot(dx, dz) || 1;
	const rimPos: [number, number, number] = [subj[0] + (dx / dl) * 2.5 + 0.6, subj[1] + 1.6, subj[2] + (dz / dl) * 2.5];
	const arm = povArmAt(t);
	const [rimTgt] = useState(() => new Object3D());
	const [spotTgt] = useState(() => new Object3D());
	return (
		<>
			<CameraRig t={t} />
			<color attach="background" args={['#6f9fc4']} />
			<fog attach="fog" args={['#79a9cc', 6, 16]} />
			<hemisphereLight args={['#d9f4ff', '#3a5f86', 1.55 * room]} />
			<directionalLight
				position={[1.8, 4.2, 3.2]}
				intensity={1.9 * room}
				color="#f2fbff"
				castShadow
				shadow-mapSize-width={1024}
				shadow-mapSize-height={1024}
				shadow-camera-left={-3.2}
				shadow-camera-right={3.2}
				shadow-camera-top={3.2}
				shadow-camera-bottom={-3.2}
				shadow-camera-near={0.5}
				shadow-camera-far={12}
				shadow-bias={-0.0004}
				shadow-radius={4}
			/>
			<pointLight position={[0, 2.35, 0.45]} intensity={2.2 * room} color="#e9f8ff" distance={6} decay={1.2} />
			<primitive object={rimTgt} position={subj as [number, number, number]} />
			<directionalLight position={rimPos} target={rimTgt} intensity={2.4} color="#ffd9a0" />
			<primitive object={spotTgt} position={[0.3, 0, 0.6]} />
			{/* always mounted (a changing light count recompiles every shader) */}
			<spotLight position={[0.3, 2.1, -3.2]} angle={0.62} penumbra={0.6} intensity={28 * out} distance={9} decay={1.4} color="#ffc27a" target={spotTgt} />
			<Set t={t} room={room} />
			{shot.showChar && <Character t={t} />}
			{shot.showChar && <Breath t={t} pose={pose} on={t > 1.6 && t < 6.84} />}
			{shot.showChar && <HeatAura t={t} pose={pose} level={heat(t)} on={auraVisible(t)} />}
			{shot.showArm && t > 9.9 && <PovArm hand={arm.hand} elbow={arm.elbow} />}
			<FrostMotes t={t} />
		</>
	);
};
