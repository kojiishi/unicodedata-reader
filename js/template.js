const u${NAME}AsInt = (function () {
  const bytes = atob("$BASE64BYTES");
  const len = bytes.length;
  const entries = []
  let value = 0;
  for (let i = 0; i < len; ++i) {
    const byte = bytes.charCodeAt(i);
    if (byte & 0x80) {
      value = (value | (byte & 0x7F)) << 7;
      continue;
    }
    value |= byte;
    entries.push((value >> $VALUE_BITS) + 1);
    entries.push(value & $VALUE_MASK);
    value = 0;
  }
  return function (c) {
    for (let i = 0; i < entries.length; i += 2) {
      c -= entries[i];
      if (c < 0)
        return entries[i + 1];
    }
  }
})();
const u${NAME}Values = [$VALUE_LIST];
function u${NAME}(c) { return u${NAME}Values[u${NAME}AsInt(c)]; }
