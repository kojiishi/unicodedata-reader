const FUNC_NAME = (function () {
  const bytes = atob('BASE64');
  const len = bytes.length;
  const entries = []
  let value = 0;
  for (let i = 0; i < len; ++i) {
    value <<= 7;
    const byte = bytes.charCodeAt(i);
    if (byte & 0x80) {
      value |= byte & 0x7F;
      continue;
    }
    value |= byte;
    const count = (value >> VALUE_BITS) + 1;
    value = value & ((1 << VALUE_BITS) - 1);
    entries.push([count, value]);
    value = 0;
  }
  return function (c) {
    for (const entry of entries) {
      c -= entry[0];
      if (c < 0)
        return entry[1];
    }
  }
})();
