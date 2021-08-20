const FUNC_NAME = (function () {
  const bytes = atob('BASE64');
  const len = bytes.length;
  const entries = []
  let current_value = 0;
  for (let i = 0; i < len; ++i) {
    const byte = bytes.charCodeAt(i);
    if (byte & 0x80) {
      current_value = (current_value << 7) | (byte & 0x7F);
      continue;
    }
    current_value = (current_value << 7) | byte;
    const count = (current_value >> VALUE_BITS) + 1;
    const value = current_value & ((1 << VALUE_BITS) - 1);
    entries.push([count, value]);
    current_value = 0;
  }
  return function (c) {
    for (const entry of entries) {
      c -= entry[0];
      if (c < 0)
        return entry[1];
    }
  }
})();
