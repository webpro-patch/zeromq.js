{
  'variables': {
    'zmq_external%': 'false',
  },
  'targets': [
    {
      'target_name': 'libzmq',
      'type': 'none',
      'actions': [{
        'action_name': 'prepare-build',
        'inputs': [],
        'conditions': [
          ['OS=="win"', {
            'outputs': ['windows/lib/libzmq.lib'],
          }, {
            'outputs': ['zmq/BUILD_SUCCESS'],
          }],
        ],
        'action': ['node', '<(PRODUCT_DIR)/../../scripts/prepare.js'],
      }],
    },
    {
      'target_name': 'zmq',
      'dependencies': ['libzmq'],
      'sources': ['binding.cc'],
      'include_dirs' : ["<!(node -e \"require('nan')\")", "${libzmq_dir}"],
      'cflags!': ['-fno-exceptions'],
      'cflags_cc!': ['-fno-exceptions'],
      'conditions': [
        ["zmq_external == 'true'", {
          'link_settings': {
            'libraries': ['${libzmq_lib}'],
          },
        }, {
          'conditions': [
            ['OS=="win"', {
              'defines': ['ZMQ_STATIC'],
              'include_dirs': ['windows/include'],
              'libraries': [
                '<(PRODUCT_DIR)/../../windows/lib/libzmq',
                'ws2_32.lib',
                'iphlpapi',
              ],
            }],
            ['OS=="mac" or OS=="solaris"', {
              'xcode_settings': {
                'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
                'MACOSX_DEPLOYMENT_TARGET': '10.15',
              },
              'libraries': ['${libzmq_lib}'],
              'include_dirs': ['${libzmq_dir}'],
            }],
            ['OS=="openbsd" or OS=="freebsd"', {
            }],
            ['OS=="linux"', {
              'libraries': ['${libzmq_lib}'],
              'include_dirs': ['${libzmq_dir}'],
            }],
          ],
        }],
      ],
    }
  ]
}
