/**
 * Profiling switches: render with --props='{"off":["gap","stipple",...]}' to drop one system and time the
 * difference (scripts/profile.sh). Never used for look decisions.
 */
import {getInputProps} from 'remotion';

let cached: string[] | null = null;
export const isOff = (k: string): boolean => {
	if (!cached) {
		try {
			const p = getInputProps() as {off?: unknown};
			cached = Array.isArray(p.off) ? (p.off as string[]) : [];
		} catch {
			cached = [];
		}
	}
	return cached.includes(k);
};
