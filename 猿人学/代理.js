const IS_PROXY = Symbol("is_proxy");

const proxyCache = new WeakMap();

function shouldSkip(obj) {
    if (!obj) return true;

    if (obj instanceof Promise) return true;

    if (typeof Node !== "undefined" && obj instanceof Node) return true;

    if (typeof obj !== "object" && typeof obj !== "function") return true;

    return false;
}

function formatValue(val) {
    if (val === undefined) return "undefined";
    if (val === null) return "null";

    const t = typeof val;

    if (t === "function") return `[Function ${val.name || "anonymous"}]`;

    if (t !== "object") return val;

    if (val instanceof Date) return `[Date ${val.toISOString()}]`;
    if (val instanceof RegExp) return `[RegExp ${val.toString()}]`;
    if (val instanceof Map) return `[Map size=${val.size}]`;
    if (val instanceof Set) return `[Set size=${val.size}]`;

    if (Array.isArray(val)) return `[Array ${val.length}]`;

    return `[Object ${val.constructor?.name || "unknown"}]`;
}

function obj_proxy(obj, name = "obj") {
    if (obj === null || obj === undefined) return obj;

    if (shouldSkip(obj)) return obj;

    if (obj[IS_PROXY]) return obj;

    if (proxyCache.has(obj)) return proxyCache.get(obj);

    const proxy = new Proxy(obj, {
        get(target, prop, receiver) {

            const value = Reflect.get(target, prop, receiver);

            console.log(`[GET] ${name}.${String(prop)} =>`, formatValue(value));

            if (typeof value === "function") {
                return func_proxy(value, `${name}.${String(prop)}`, target);
            }

            if (typeof value === "object" && value !== null && !shouldSkip(value)) {
                return obj_proxy(value, `${name}.${String(prop)}`);
            }

            return value;
        },

        set(target, prop, value, receiver) {
            console.log(`[SET] ${name}.${String(prop)} =`, formatValue(value));
            return Reflect.set(target, prop, value, receiver);
        },

        has(target, prop) {
            const res = Reflect.has(target, prop);
            console.log(`[HAS] ${name} has ${String(prop)} =>`, res);
            return res;
        },

        deleteProperty(target, prop) {
            console.log(`[DELETE] ${name}.${String(prop)}`);
            return Reflect.deleteProperty(target, prop);
        },

        ownKeys(target) {
            const keys = Reflect.ownKeys(target);
            console.log(`[KEYS] ${name}`, keys);
            return keys;
        }
    });

    Object.defineProperty(proxy, IS_PROXY, {
        value: true,
        enumerable: false
    });

    proxyCache.set(obj, proxy);

    return proxy;
}

function func_proxy(func, name, bindObj = null) {
    if (proxyCache.has(func)) return proxyCache.get(func);

    const proxy = new Proxy(func, {
        apply(target, thisArg, args) {
            console.log(`[CALL] ${name}(${args.map(formatValue).join(", ")})`);

            const realThis = bindObj || thisArg;

            const ret = Reflect.apply(target, realThis, args);

            console.log(`[RETURN] ${name} =>`, formatValue(ret));

            if (ret && typeof ret === "object" && !shouldSkip(ret)) {
                return obj_proxy(ret, `${name}()`);
            }

            return ret;
        },

        construct(target, args) {
            console.log(`[NEW] ${name}(${args.map(formatValue).join(", ")})`);
            const instance = new target(...args);
            return obj_proxy(instance, `new ${name}`);
        }
    });

    proxyCache.set(func, proxy);
    return proxy;
}


window = global;
delete global;

document = {};
navigator = {}
location = {};

window = obj_proxy(window, "window");
document = obj_proxy(document, "document");
navigator = obj_proxy(navigator, "navigator");
location = obj_proxy(location, "location");

