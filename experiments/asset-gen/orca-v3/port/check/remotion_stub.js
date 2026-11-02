module.exports = {Easing: new Proxy({}, {get: () => (x) => x}), spring: () => 1, random: () => 0.5, interpolate: (x) => x};
